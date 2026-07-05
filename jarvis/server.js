const express = require('express');
const http = require('http');
const path = require('path');
const { WebSocketServer } = require('ws');
const { think } = require('./brain');

const PORT = process.env.PORT || 4000;

const app = express();
app.use(express.static(path.join(__dirname, 'public')));

const server = http.createServer(app);
const wss = new WebSocketServer({ server, path: '/ws' });

wss.on('connection', (ws) => {
  ws.on('message', (raw) => {
    let msg;
    try {
      msg = JSON.parse(raw);
    } catch {
      return;
    }
    if (msg.type !== 'command' || typeof msg.text !== 'string') return;

    const reply = think(msg.text);
    ws.send(JSON.stringify({ type: 'response', text: reply }));
  });
});

server.listen(PORT, () => {
  console.log(`Jarvis läuft auf http://localhost:${PORT}`);
});
