// Simple auto-hide for flash messages
document.addEventListener("DOMContentLoaded", () => {
  const alerts = document.querySelectorAll(".flash-message");
  if (!alerts.length) return;

  setTimeout(() => {
    alerts.forEach(a => {
      a.classList.add("fade");
      setTimeout(() => a.remove(), 300);
    });
  }, 3000);
});
