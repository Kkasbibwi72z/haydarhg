// Platzhalter-"Gehirn" von Jarvis, solange kein ANTHROPIC_API_KEY hinterlegt ist.
// Sobald du einen Key aus console.anthropic.com in jarvis/.env einträgst
// (ANTHROPIC_API_KEY=...), ersetze die think()-Funktion unten durch einen
// echten Aufruf der Claude API (@anthropic-ai/sdk), die statt der
// Regel-Erkennung freie Sprache versteht.

function think(text) {
  const t = text.toLowerCase();

  if (t.includes('hallo') || t.includes('hey jarvis') || t.includes('guten tag')) {
    return 'Hallo. Ich höre zu, wie kann ich helfen?';
  }

  if (t.includes('wie geht') && t.includes('dir')) {
    return 'Mir geht es gut, danke der Nachfrage. Wie kann ich dir helfen?';
  }

  if (t.includes('wer bist du')) {
    return 'Ich bin Jarvis, dein Sprachassistent.';
  }

  return 'Das habe ich noch nicht gelernt. Sobald ein Claude API-Key hinterlegt ist, kann ich beliebige Fragen beantworten.';
}

module.exports = { think };
