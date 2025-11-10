class CustomMessage extends BaseComponent {
  template() {
    const { message } = this._state;

    if (!message) {
      return '<div></div>';
    }

    return `
      <div class="custom-message">
        <div class="custom-message-text">${message}</div>
      </div>
    `;
  }

  constructor() {
    super();
    this.setState({
      visible: false,
      message: ''
    });
  }

  static get observedAttributes() {
    return ['visible', 'message'];
  }

  attributeChangedCallback(name, oldValue, newValue) {
    if (name === 'visible') {
      this.setState({ visible: newValue !== null });
    } else if (name === 'message') {
      this.setState({ message: newValue || '' });
    }
  }

  show(message) {
    this.setState({
      visible: true,
      message: message || ''
    });
    this.classList.add('visible');
  }

  hide() {
    this.setState({ visible: false });
    this.classList.remove('visible');
  }

  updateMessage(message) {
    this.setState({ message: message || '' });
  }

  styles() {
    return `
      :host {
        display: block;
        position: absolute;
        top: 40px;
        left: 50%;
        transform: translateX(-50%) translateY(-100%);
        opacity: 0;
        transition: all 0.5s ease;
        max-width: 80%;
      }

      :host(.visible) {
        opacity: 1;
        transform: translateX(-50%) translateY(0);
      }

      .custom-message {
        background: linear-gradient(135deg, rgba(255, 170, 0, 0.95), rgba(255, 136, 0, 0.95));
        border-radius: 10px;
        padding: 15px 30px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        border: 2px solid rgba(255, 255, 255, 0.3);
      }

      .custom-message-text {
        font-size: 24px;
        font-weight: bold;
        color: white;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        text-align: center;
      }
    `;
  }
}

customElements.define('custom-message', CustomMessage);
