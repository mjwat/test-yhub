const button = document.getElementById('cta');
const message = document.getElementById('message');

button?.addEventListener('click', () => {
  message.textContent = 'Interaction complete. Now deploy it.';
});