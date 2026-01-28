// Robô WhatsApp - Página de Envio

let tempFile = null;
let totalContatos = 0;
let socket = null;
let sessionId = null;

// Inicializa Socket.IO
function initSocket() {
    socket = io();
    
    socket.on('status_update', (data) => {
        if (data.session_id === sessionId) {
            document.getElementById('statusText').textContent = data.message;
        }
    });
    
    socket.on('progresso_update', (data) => {
        if (data.session_id === sessionId) {
            const progresso = (data.atual / data.total) * 100;
            document.getElementById('progressFill').style.width = progresso + '%';
            document.getElementById('progressAtual').textContent = data.atual;
            document.getElementById('progressTotal').textContent = data.total;
            document.getElementById('statusText').textContent = `Enviando para ${data.nome} (${data.contato})`;
        }
    });
    
    socket.on('mensagem_enviada', (data) => {
        if (data.session_id === sessionId) {
            const logArea = document.getElementById('logArea');
            const logItem = document.createElement('div');
            logItem.className = `log-item ${data.sucesso ? 'success' : 'error'}`;
            logItem.innerHTML = `
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    ${data.sucesso ? 
                        '<polyline points="20 6 9 17 4 12"></polyline>' :
                        '<circle cx="12" cy="12" r="10"></circle><line x1="15" y1="9" x2="9" y2="15"></line><line x1="9" y1="9" x2="15" y2="15"></line>'
                    }
                </svg>
                <span>${data.nome} (${data.contato}) - ${data.sucesso ? 'Enviado' : data.motivo}</span>
            `;
            logArea.appendChild(logItem);
            logArea.scrollTop = logArea.scrollHeight;
            
            // Atualiza estatísticas
            if (data.sucesso) {
                const enviados = parseInt(document.getElementById('statEnviados').textContent) + 1;
                document.getElementById('statEnviados').textContent = enviados;
            } else {
                const falhas = parseInt(document.getElementById('statFalhas').textContent) + 1;
                document.getElementById('statFalhas').textContent = falhas;
            }
        }
    });
    
    socket.on('envio_concluido', (data) => {
        if (data.session_id === sessionId) {
            mostrarResultado(data);
        }
    });
    
    socket.on('erro_envio', (data) => {
        if (data.session_id === sessionId) {
            alert('Erro no envio: ' + data.message);
            location.reload();
        }
    });
}

// Upload de arquivo
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');

uploadArea.addEventListener('click', () => {
    fileInput.click();
});

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFile(e.target.files[0]);
    }
});

async function handleFile(file) {
    if (!file.name.endsWith('.xlsx')) {
        alert('Apenas arquivos .xlsx são aceitos');
        return;
    }
    
    const formData = new FormData();
    formData.append('planilha', file);
    
    try {
        const response = await fetch('/api/validar-planilha', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            tempFile = data.temp_file;
            totalContatos = data.total;
            
            // Mostra informações do arquivo
            document.getElementById('fileName').textContent = file.name;
            document.getElementById('fileSize').textContent = formatBytes(file.size);
            document.getElementById('fileInfo').style.display = 'flex';
            document.getElementById('uploadArea').style.display = 'none';
            
            // Mostra preview
            mostrarPreview(data.preview, data.total);
            
            // Mostra próximo passo
            document.getElementById('step2').style.display = 'block';
            document.getElementById('step2').scrollIntoView({ behavior: 'smooth' });
        } else {
            alert('Erro: ' + data.message);
        }
    } catch (error) {
        console.error('Erro:', error);
        alert('Erro ao validar planilha');
    }
}

function formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

function mostrarPreview(preview, total) {
    const tbody = document.getElementById('previewBody');
    tbody.innerHTML = '';
    
    preview.forEach(item => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${item.nome || '-'}</td>
            <td>${item.contato}</td>
        `;
        tbody.appendChild(tr);
    });
    
    document.getElementById('totalContatos').textContent = total;
    document.getElementById('previewArea').style.display = 'block';
}

function removerArquivo() {
    tempFile = null;
    totalContatos = 0;
    fileInput.value = '';
    document.getElementById('fileInfo').style.display = 'none';
    document.getElementById('uploadArea').style.display = 'flex';
    document.getElementById('previewArea').style.display = 'none';
    document.getElementById('step2').style.display = 'none';
    document.getElementById('step3').style.display = 'none';
}

// Mensagem
const mensagemInput = document.getElementById('mensagem');
const charCount = document.getElementById('charCount');
const messagePreview = document.getElementById('messagePreview');

mensagemInput.addEventListener('input', () => {
    const texto = mensagemInput.value;
    const tamanho = texto.length;
    
    charCount.textContent = tamanho;
    charCount.style.color = tamanho > 4096 ? 'var(--error)' : 'var(--text-secondary)';
    
    // Preview
    if (texto.trim()) {
        const preview = texto.replace('{}', 'João Silva');
        messagePreview.textContent = preview;
    } else {
        messagePreview.textContent = 'Digite sua mensagem para ver o preview...';
    }
    
    // Mostra próximo passo se tiver mensagem
    if (texto.trim() && tempFile) {
        document.getElementById('step3').style.display = 'block';
        document.getElementById('resumoTotal').textContent = totalContatos;
        document.getElementById('resumoTamanho').textContent = tamanho + ' caracteres';
    }
});

// Iniciar envio
async function iniciarEnvio() {
    const mensagem = mensagemInput.value.trim();
    
    if (!tempFile) {
        alert('Selecione uma planilha primeiro');
        return;
    }
    
    if (!mensagem) {
        alert('Digite uma mensagem');
        return;
    }
    
    if (mensagem.length > 4096) {
        alert('Mensagem muito longa (máximo 4096 caracteres)');
        return;
    }
    
    if (!confirm(`Enviar mensagem para ${totalContatos} contatos?`)) {
        return;
    }
    
    // Inicializa socket
    initSocket();
    
    // Oculta formulário e mostra progresso
    document.getElementById('step1').style.display = 'none';
    document.getElementById('step2').style.display = 'none';
    document.getElementById('step3').style.display = 'none';
    document.getElementById('progressArea').style.display = 'block';
    
    try {
        const response = await fetch('/api/iniciar-envio', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                temp_file: tempFile,
                mensagem: mensagem
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            sessionId = data.session_id;
            document.getElementById('progressTotal').textContent = totalContatos;
        } else {
            alert('Erro: ' + data.message);
            location.reload();
        }
    } catch (error) {
        console.error('Erro:', error);
        alert('Erro ao iniciar envio');
        location.reload();
    }
}

function mostrarResultado(data) {
    document.getElementById('progressArea').style.display = 'none';
    document.getElementById('resultArea').style.display = 'block';
    
    document.getElementById('resultEnviados').textContent = data.enviados;
    document.getElementById('resultFalhas').textContent = data.falhas;
    document.getElementById('resultTotal').textContent = data.total;
    
    document.getElementById('resultArea').scrollIntoView({ behavior: 'smooth' });
}
