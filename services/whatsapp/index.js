const express = require('express');
const cors = require('cors');
const axios = require('axios');
const { makeWASocket, useMultiFileAuthState, DisconnectReason } = require('@whiskeysockets/baileys');

const app = express();
app.use(cors());
app.use(express.json());

const PORT = process.env.PORT || 3001;
const GATEWAY_URL = process.env.GATEWAY_URL || 'http://localhost:8080/api/mcp/message';

let qrCodeData = null;
let connectionStatus = 'disconnected'; // disconnected, connecting, connected
let sock = null;

async function connectToWhatsApp() {
  const { state, saveCreds } = await useMultiFileAuthState('auth_info_baileys');
  
  sock = makeWASocket({
    auth: state,
    printQRInTerminal: true,
  });

  sock.ev.on('creds.update', saveCreds);

  sock.ev.on('connection.update', (update) => {
    const { connection, lastDisconnect, qr } = update;
    
    if (qr) {
      qrCodeData = qr;
      connectionStatus = 'connecting';
    }

    if (connection === 'close') {
      const shouldReconnect = (lastDisconnect?.error?.output?.statusCode !== DisconnectReason.loggedOut);
      connectionStatus = 'disconnected';
      qrCodeData = null;
      if (shouldReconnect) {
        connectToWhatsApp();
      }
    } else if (connection === 'open') {
      connectionStatus = 'connected';
      qrCodeData = null;
      console.log('WhatsApp connection opened successfully!');
    }
  });

  sock.ev.on('messages.upsert', async (m) => {
    if (m.type === 'notify') {
      for (const msg of m.messages) {
        if (!msg.key.fromMe && msg.message) {
          const text = msg.message.conversation || msg.message.extendedTextMessage?.text || '';
          const sender = msg.key.remoteJid;

          if (text) {
            console.log(`Received message from ${sender}: ${text}`);
            
            try {
              // Enviar al Gateway de OpenClaw con el agente bilingüe
              const response = await axios.post(GATEWAY_URL, {
                agent: 'bilingual_cs',
                message: text,
                session_id: sender
              });

              const replyText = response.data?.response;
              if (replyText) {
                await sock.sendMessage(sender, { text: replyText });
                console.log(`Replied to ${sender}: ${replyText}`);
              }
            } catch (err) {
              console.error('Error enviando mensaje al Gateway de OpenClaw:', err.message);
            }
          }
        }
      }
    }
  });
}

// Endpoints para el Panel Visual (Integraciones UI)
app.get('/api/whatsapp/status', (req, res) => {
  res.json({
    status: connectionStatus,
    qr: qrCodeData
  });
});

app.post('/api/whatsapp/connect', (req, res) => {
  if (connectionStatus === 'disconnected') {
    connectToWhatsApp();
  }
  res.json({ status: connectionStatus, message: 'Iniciando conexión WhatsApp' });
});

app.listen(PORT, () => {
  console.log(`Servicio OpenClaw WhatsApp listo en el puerto ${PORT}`);
});
