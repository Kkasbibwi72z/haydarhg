const reactor = document.getElementById('reactor');
const statusEl = document.getElementById('status');
const talkBtn = document.getElementById('talkBtn');
const logEl = document.getElementById('log');

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
let recognition = null;
let listening = false;

if (SpeechRecognition) {
  recognition = new SpeechRecognition();
  recognition.lang = 'de-DE';
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;

  recognition.onresult = (event) => {
    const text = event.results[0][0].transcript;
    log('you', text);
    sendCommand(text);
  };

  recognition.onerror = (event) => {
    setStatus('Fehler bei der Spracherkennung: ' + event.error);
  };

  recognition.onend = () => {
    listening = false;
    reactor.classList.remove('listening');
    talkBtn.classList.remove('active');
  };
} else {
  setStatus('Dieser Browser unterstützt keine Spracherkennung. Bitte Chrome verwenden.');
}

function startListening() {
  if (!recognition || listening) return;
  listening = true;
  reactor.classList.add('listening');
  talkBtn.classList.add('active');
  setStatus('Ich höre zu...');
  recognition.start();
}

function stopListening() {
  if (!recognition || !listening) return;
  recognition.stop();
}

talkBtn.addEventListener('mousedown', startListening);
talkBtn.addEventListener('mouseup', stopListening);
talkBtn.addEventListener('mouseleave', () => { if (listening) stopListening(); });
talkBtn.addEventListener('touchstart', (e) => { e.preventDefault(); startListening(); });
talkBtn.addEventListener('touchend', (e) => { e.preventDefault(); stopListening(); });

document.addEventListener('keydown', (e) => {
  if (e.code === 'Space' && !e.repeat) { e.preventDefault(); startListening(); }
});
document.addEventListener('keyup', (e) => {
  if (e.code === 'Space') { e.preventDefault(); stopListening(); }
});

function setStatus(text) {
  statusEl.textContent = text;
}

function log(kind, text) {
  const line = document.createElement('div');
  line.className = kind;
  const label = kind === 'you' ? 'Du' : kind === 'jarvis' ? 'Jarvis' : 'System';
  line.textContent = `${label}: ${text}`;
  logEl.appendChild(line);
  logEl.scrollTop = logEl.scrollHeight;
}

// --- WebSocket-Verbindung zum lokalen Server ---

let ws;
function connect() {
  ws = new WebSocket(`ws://${location.host}/ws`);

  ws.onopen = () => setStatus('Verbunden. Halte die Taste zum Sprechen.');

  ws.onclose = () => {
    setStatus('Verbindung verloren, versuche erneut...');
    setTimeout(connect, 1500);
  };

  ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);

    if (msg.type === 'response') {
      log('jarvis', msg.text);
      speak(msg.text);
      setStatus('Bereit. Halte die Taste zum Sprechen.');
    }
  };
}
connect();

function sendCommand(text) {
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({ type: 'command', text }));
  }
}

// --- Sprachausgabe ---

let jarvisVoice = null;
function pickVoice() {
  const voices = speechSynthesis.getVoices();
  jarvisVoice =
    voices.find(v => /David|Male|George/i.test(v.name) && v.lang.startsWith('de')) ||
    voices.find(v => /Male/i.test(v.name)) ||
    voices.find(v => v.lang.startsWith('de')) ||
    voices[0] || null;
}
speechSynthesis.onvoiceschanged = pickVoice;
pickVoice();

function speak(text) {
  if (!('speechSynthesis' in window)) return;
  const utter = new SpeechSynthesisUtterance(text);
  if (jarvisVoice) utter.voice = jarvisVoice;
  utter.pitch = 0.8;
  utter.rate = 1.0;

  reactor.classList.add('speaking');
  utter.onend = () => reactor.classList.remove('speaking');

  speechSynthesis.speak(utter);
}
