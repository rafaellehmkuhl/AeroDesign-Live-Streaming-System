class FlightResults extends BaseComponent {
  template() {
    const { results } = this._state;

    const resultsHtml = results.length === 0
      ? '<div class="no-results">Nenhum resultado disponível</div>'
      : results.map(result => `
          <div class="result-item ${result.status}">
            <span class="result-battery">Bateria ${result.battery_number}</span>
            <span class="result-status">${this.statusTranslations[result.status] || result.status}</span>
            <span class="result-score">${result.score !== null && result.score !== undefined ? result.score.toFixed(1) : '-'}</span>
          </div>
        `).join('');

    return `
      <div class="flight-results">
        <div class="results-title">Resultados dos Voos</div>
        <div class="results-container">
          ${resultsHtml}
        </div>
      </div>
    `;
  }

  constructor() {
    super();
    this.setState({
      visible: false,
      results: []
    });

    this.statusTranslations = {
      'validated': 'Validado',
      'invalidated': 'Invalidado',
      'pending': 'Em andamento',
      'not_flown': 'Não voado'
    };
  }

  static get observedAttributes() {
    return ['visible'];
  }

  attributeChangedCallback(name, oldValue, newValue) {
    if (name === 'visible') {
      this.setState({ visible: newValue !== null });
    }
  }

  show(results) {
    this.setState({
      visible: true,
      results: results || []
    });
    this.classList.add('visible');
  }

  hide() {
    this.setState({ visible: false });
    this.classList.remove('visible');
  }

  updateResults(results) {
    this.setState({ results: results || [] });
  }

  styles() {
    return `
      :host {
        display: block;
        position: absolute;
        top: 50%;
        right: 40px;
        transform: translateY(-50%) translateX(100%);
        opacity: 0;
        transition: all 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        transition-delay: 0.2s;
      }

      :host(.visible) {
        opacity: 1;
        transform: translateY(-50%) translateX(0);
      }

      .flight-results {
        background: rgba(0, 0, 0, 0.85);
        border-radius: 15px;
        padding: 20px;
        min-width: 400px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        border: 2px solid rgba(255, 255, 255, 0.1);
      }

      .results-title {
        font-size: 20px;
        font-weight: bold;
        color: white;
        margin-bottom: 15px;
        text-transform: uppercase;
        letter-spacing: 1px;
      }

      .result-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 12px 15px;
        margin-bottom: 10px;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.05);
        border-left: 4px solid;
        transition: all 0.3s;
      }

      .result-item:last-child {
        margin-bottom: 0;
      }

      .result-item.validated {
        border-left-color: #00cc66;
      }

      .result-item.invalidated {
        border-left-color: #cc0000;
      }

      .result-item.pending {
        border-left-color: #ffaa00;
        animation: pulse 2s infinite;
      }

      .result-item.not_flown {
        border-left-color: #666666;
      }

      @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
      }

      .result-battery {
        font-size: 16px;
        font-weight: bold;
        color: white;
        margin-right: 10px;
      }

      .result-status {
        flex: 1;
        font-size: 14px;
        color: rgba(255, 255, 255, 0.9);
      }

      .result-score {
        font-size: 20px;
        font-weight: bold;
        color: white;
        min-width: 60px;
        text-align: right;
      }

      .no-results {
        color: rgba(255, 255, 255, 0.6);
        text-align: center;
        padding: 10px;
      }
    `;
  }
}

customElements.define('flight-results', FlightResults);
