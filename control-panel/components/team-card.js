class TeamCard extends BaseComponent {
  template() {
    const { teamData, active } = this._state;

    if (!teamData) {
      return '<div></div>';
    }

    return `
      <div class="team-card ${active ? 'active' : ''}">
        <h3>${teamData.name}</h3>
        <p>${teamData.university}</p>
        <span class="battery">Bateria ${teamData.current_battery}</span>
      </div>
    `;
  }

  constructor() {
    super();
    this.setState({
      teamData: null,
      active: false
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

  afterRender() {
    const card = this.$('.team-card');
    if (card) {
      card.addEventListener('click', () => {
        this.emit('team-selected', { teamId: this._state.teamData.id });
      });
    }
  }

  setTeam(teamData) {
    this.setState({ teamData });
  }

  setActive(active) {
    this.setState({ active });
  }

  styles() {
    return `
      :host {
        display: block;
      }

      .team-card {
        background: #f8f9fa;
        border: 2px solid #e0e0e0;
        border-radius: 8px;
        padding: 15px;
        cursor: pointer;
        transition: all 0.3s;
      }

      .team-card:hover {
        border-color: #667eea;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
      }

      .team-card.active {
        border-color: #00cc66;
        background: #e8f8f1;
      }

      .team-card h3 {
        color: #333;
        margin-bottom: 5px;
        font-size: 18px;
      }

      .team-card p {
        color: #666;
        font-size: 13px;
        margin-bottom: 8px;
      }

      .team-card .battery {
        display: inline-block;
        background: #667eea;
        color: white;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
      }
    `;
  }
}

customElements.define('team-card', TeamCard);
