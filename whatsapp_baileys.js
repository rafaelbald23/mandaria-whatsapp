/**
 * WhatsApp Baileys - Servidor WebSocket integrado
 * Substitui a necessidade de Evolution API externa
 */

const { default: makeWASocket, DisconnectReason, useMultiFileAuthState } = require('@whiskeysockets/baileys');
const { Boom } = require('@hapi/boom');
const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const fs = require('fs');
const path = require('path');

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
    cors: {
        origin: "*",
        methods: ["GET", "POST"]
    }
});

app.use(express.json());

let sock = null;
let qrCode = null;
let isConnected = false;

// Diretório para salvar sessão
const SESSION_DIR = path.join(__dirname, 'baileys_session');
if (!fs.existsSync(SESSION_DIR)) {
    fs.mkdirSync(SESSION_DIR, { recursive: true });
}

async function connectToWhatsApp() {
    const { state, saveCreds } = await useMultiFileAuthState(SESSION_DIR);
    
    sock = makeWASocket({
        auth: state,
        printQRInTerminal: true
    });

    sock.ev.on('connection.update', (update) => {
        const { connection, lastDisconnect, qr } = update;
        
        if (qr) {
            qrCode = qr;
            console.log('QR Code gerado!');
            io.emit('qr', qr);
        }
        
        if (connection === 'close') {
            const shouldReconnect = (lastDisconnect?.error instanceof Boom)?.output?.statusCode !== DisconnectReason.loggedOut;
            console.log('Conexão fechada. Reconectando:', shouldReconnect);
            
            isConnected = false;
            io.emit('disconnected');
            
            if (shouldReconnect) {
                connectToWhatsApp();
            }
        } else if (connection === 'open') {
            console.log('Conectado ao WhatsApp!');
            isConnected = true;
            qrCode = null;
            io.emit('connected');
        }
    });

    sock.ev.on('creds.update', saveCreds);
}

// API REST
app.get('/status', (req, res) => {
    res.json({
        connected: isConnected,
        hasQR: !!qrCode
    });
});

app.get('/qr', (req, res) => {
    if (qrCode) {
        res.json({ qr: qrCode });
    } else {
        res.status(404).json({ error: 'QR Code não disponível' });
    }
});

app.post('/send', async (req, res) => {
    try {
        if (!isConnected) {
            return res.status(400).json({ error: 'WhatsApp não conectado' });
        }

        const { number, message } = req.body;
        
        if (!number || !message) {
            return res.status(400).json({ error: 'Número e mensagem são obrigatórios' });
        }

        // Formata número
        const formattedNumber = number.includes('@s.whatsapp.net') 
            ? number 
            : `${number}@s.whatsapp.net`;

        // Envia mensagem
        await sock.sendMessage(formattedNumber, { text: message });
        
        res.json({ success: true, message: 'Mensagem enviada' });
    } catch (error) {
        console.error('Erro ao enviar mensagem:', error);
        res.status(500).json({ error: error.message });
    }
});

app.post('/send-image', async (req, res) => {
    try {
        if (!isConnected) {
            return res.status(400).json({ error: 'WhatsApp não conectado' });
        }

        const { number, image, caption } = req.body;
        
        if (!number || !image) {
            return res.status(400).json({ error: 'Número e imagem são obrigatórios' });
        }

        const formattedNumber = number.includes('@s.whatsapp.net') 
            ? number 
            : `${number}@s.whatsapp.net`;

        // Converte base64 para buffer
        const imageBuffer = Buffer.from(image, 'base64');

        await sock.sendMessage(formattedNumber, {
            image: imageBuffer,
            caption: caption || ''
        });
        
        res.json({ success: true, message: 'Imagem enviada' });
    } catch (error) {
        console.error('Erro ao enviar imagem:', error);
        res.status(500).json({ error: error.message });
    }
});

app.post('/logout', async (req, res) => {
    try {
        if (sock) {
            await sock.logout();
            // Remove sessão
            if (fs.existsSync(SESSION_DIR)) {
                fs.rmSync(SESSION_DIR, { recursive: true, force: true });
            }
        }
        isConnected = false;
        qrCode = null;
        res.json({ success: true, message: 'Logout realizado' });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// WebSocket
io.on('connection', (socket) => {
    console.log('Cliente conectado via WebSocket');
    
    // Envia status atual
    socket.emit('status', {
        connected: isConnected,
        hasQR: !!qrCode
    });
    
    if (qrCode) {
        socket.emit('qr', qrCode);
    }
    
    socket.on('disconnect', () => {
        console.log('Cliente desconectado');
    });
});

// Inicia servidor
const PORT = process.env.BAILEYS_PORT || 3000;
server.listen(PORT, () => {
    console.log(`Servidor Baileys rodando na porta ${PORT}`);
    connectToWhatsApp();
});
