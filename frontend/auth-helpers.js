window.OnlyWayOutAuth = {
  validateEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  },
  setStatus(element, message, type = 'info') {
    if (!element) return;
    element.textContent = message;
    element.className = 'status-message';
    element.classList.add(type === 'error' ? 'status-error' : type === 'success' ? 'status-success' : 'status-info');
  },
  setLoading(button, isLoading, label = 'Please wait...') {
    if (!button) return;
    button.disabled = isLoading;
    if (isLoading) {
      button.dataset.originalText = button.textContent;
      button.textContent = label;
      return;
    }
    button.textContent = button.dataset.originalText || button.textContent;
  }
};
