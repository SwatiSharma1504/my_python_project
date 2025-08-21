const chat = document.getElementById('chat');
const input = document.getElementById('userInput');
const toggleDark = document.getElementById('toggleDark');
const uploadFile = document.getElementById('uploadFile');
const downloadBtn = document.getElementById('downloadChat');
const sidebarToggle = document.getElementById('sidebarToggle');
const sidebar = document.getElementById('sidebar');
const closeSidebar = document.getElementById('closeSidebar');
let chatHistory = JSON.parse(localStorage.getItem('jarvis_history') || '[]');
function saveHistory(user, bot) {
  chatHistory.push({ user, bot });
  if (chatHistory.length > 20) chatHistory.shift(); // keep last 20
  localStorage.setItem('jarvis_history', JSON.stringify(chatHistory));
  renderHistory();
}
function renderHistory() {
  const historyDiv = document.getElementById('chatHistory');
  if (!historyDiv) return;
  historyDiv.innerHTML = '';
  chatHistory.slice().reverse().forEach((item, idx) => {
    const div = document.createElement('div');
    div.className = 'history-item';
    div.title = item.user;
    div.textContent = item.user.length > 32 ? item.user.slice(0, 32) + '…' : item.user;
    div.onclick = () => {
      chat.innerHTML = '';
      addMessage(item.user, 'user');
      addMessage(item.bot, 'bot');
    };
    historyDiv.appendChild(div);
  });
}
renderHistory();
async function sendMessage() {
  const userText = input.value.trim();
  if (!userText) return;
  addMessage(userText, 'user');
  input.value = '';
  input.focus();
  chat.scrollTop = chat.scrollHeight;
  const typingMsg = addMessage("Jarvis is typing...", 'bot');
  typingMsg.classList.add("typing");
  await new Promise(res => setTimeout(res, 400));
  try {
    const response = await fetch('http://127.0.0.1:5000/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: userText })
    });
    const data = await response.json();
    typingMsg.remove();
    addMessage(data.reply, 'bot');
    saveHistory(userText, data.reply);
  } catch (err) {
    typingMsg.remove();
    addMessage("Something went wrong!", 'bot');
  }
  chat.scrollTop = chat.scrollHeight;
}
function addMessage(text, type) {
  const msg = document.createElement('div');
  msg.className = `message ${type}`;
  const avatar = document.createElement('div');
  avatar.className = `avatar ${type}`;
  avatar.textContent = type === 'user' ? '🧑' : '🤖';
  const bubble = document.createElement('div');
  bubble.className = 'bubble';
  bubble.textContent = text;
  msg.appendChild(avatar);
  msg.appendChild(bubble);
  chat.appendChild(msg);
  chat.scrollTop = chat.scrollHeight;
  return msg;
}
toggleDark.onclick = () => {
  document.body.classList.toggle('dark-mode');
};
downloadBtn.onclick = () => {
  let content = '';
  document.querySelectorAll('.message').forEach(msg => {
    const isUser = msg.classList.contains('user');
    const bubble = msg.querySelector('.bubble');
    content += (isUser ? 'You: ' : 'Jarvis: ') + (bubble ? bubble.textContent : msg.textContent) + '\n';
  });
  const blob = new Blob([content], { type: 'text/plain' });
  const link = document.createElement('a');
  link.download = 'jarvis_chat.txt';
  link.href = URL.createObjectURL(blob);
  link.click();
};
uploadFile.onchange = async () => {
  const file = uploadFile.files[0];
  if (!file) return;
  const formData = new FormData();
  formData.append('file', file);
  try {
    const res = await fetch('/upload', { method: 'POST', body: formData });
    const data = await res.json();
    addMessage(`Uploaded: ${file.name}`, 'user');
    addMessage(data.reply || 'File uploaded successfully.', 'bot');
  } catch (e) {
    addMessage('Upload failed.', 'bot');
  }
};
sidebarToggle.onclick = () => {
  sidebar.classList.toggle('active');
  closeSidebar.style.display = sidebar.classList.contains('active') ? 'block' : 'none';
};
if (closeSidebar) {
  closeSidebar.onclick = () => {
    sidebar.classList.remove('active');
    closeSidebar.style.display = 'none';
  };
}
input.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') sendMessage();
});
window.addEventListener('DOMContentLoaded', () => {
  if (chatHistory.length === 0) {
    const initialBotMsg = "Hello! I am Jarvis, your AI assistant. How can I help you?";
    saveHistory('', initialBotMsg);
  }
});