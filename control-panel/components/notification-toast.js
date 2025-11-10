class NotificationToast extends BaseComponent {
  template() {
    const { visible, message, type } = this._state;

    return `
      <div class="notification ${type} ${visible ? 'visible' : ''}">
        ${message}
      </div>
    `;
  }

  constructor() {
    super();
    this.setState({
      visible: false,
      message: '',
      type: 'success'
    });
    this.hideTimeout = null;
  }

  connectedCallback() {
    this.render();
    window.showNotification = (message, type) => this.show(message, type);
  }

  show(message, type = 'success', duration = 3000) {
    if (this.hideTimeout) {
      clearTimeout(this.hideTimeout);
    }

    this.setState({
      visible: true,
      message,
      type
    });

    this.hideTimeout = setTimeout(() => {
      this.hide();
    }, duration);
  }

  hide() {
    this.setState({ visible: false });
  }

  styles() {
    return `
      :host {
        display: block;
      }

      .notification {
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 8px;
        color: white;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        opacity: 0;
        transform: translateX(100%);
        transition: all 0.3s;
        z-index: 1000;
        min-width: 200px;
      }

      .notification.visible {
        opacity: 1;
        transform: translateX(0);
      }

      .notification.success {
        background: #00cc66;
      }

      .notification.error {
        background: #ff4757;
      }
    `;
  }
}

customElements.define('notification-toast', NotificationToast);
