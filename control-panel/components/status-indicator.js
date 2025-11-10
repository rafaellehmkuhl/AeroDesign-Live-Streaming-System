class StatusIndicator extends BaseComponent {
  template() {
    const { active, statusText, teamInfo } = this._state;

    return `
      <div class="current-status">
        <h3>
          <span class="status-indicator ${active ? 'active' : 'inactive'}"></span>
          <span>${statusText}</span>
        </h3>
        <p>${teamInfo}</p>
      </div>
    `;
  }

  constructor() {
    super();
    this.setState({
      active: false,
      statusText: 'Carregando...',
      teamInfo: 'Nenhuma equipe selecionada'
    });
  }

  static get observedAttributes() {
    return ['active'];
  }

  attributeChangedCallback(name, oldValue, newValue) {
    if (name === 'active') {
      this.setState({ active: newValue !== null });
    }
  }

  updateStatus(visible, teamData = null) {
    const statusText = visible ? 'Overlay Visível' : 'Overlay Oculto';
    const teamInfo = teamData
      ? `Equipe: ${teamData.name} (Bateria ${teamData.current_battery})`
      : 'Nenhuma equipe selecionada';

    this.setState({
      active: visible,
      statusText,
      teamInfo
    });
  }

  styles() {
    return `
      :host {
        display: block;
      }

      .current-status {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
      }

      .current-status h3 {
        color: #333;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
      }

      .current-status p {
        color: #666;
        margin: 0;
      }

      .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
      }

      .status-indicator.active {
        background: #00cc66;
        animation: pulse 2s infinite;
      }

      .status-indicator.inactive {
        background: #ff4757;
      }

      @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
      }
    `;
  }
}

customElements.define('status-indicator', StatusIndicator);
