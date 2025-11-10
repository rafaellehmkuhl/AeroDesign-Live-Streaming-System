class TeamInfoCard extends BaseComponent {
  template() {
    const { teamData, showBattery } = this._state;

    if (!teamData) {
      return '<div></div>';
    }

    return `
      <div class="team-info-card">
        <div class="team-header">
          ${teamData.aircraft_photo_url ? `
            <img src="${teamData.aircraft_photo_url}"
                 alt="Aircraft"
                 class="team-photo">
          ` : ''}
          <div class="team-details">
            <div class="team-name">${teamData.name}</div>
            <div class="team-university">${teamData.university}</div>
            ${showBattery ? `
              <div class="current-battery">
                <span class="current-battery-label">Bateria Atual:</span>
                <span class="current-battery-number">${teamData.current_battery}</span>
              </div>
            ` : ''}
          </div>
        </div>
      </div>
    `;
  }

  constructor() {
    super();
    this.setState({
      visible: false,
      teamData: null,
      showBattery: true
    });
  }

  static get observedAttributes() {
    return ['visible'];
  }

  attributeChangedCallback(name, oldValue, newValue) {
    if (name === 'visible') {
      this.setState({ visible: newValue !== null });
    }
  }

  show(teamData, showBattery = true) {
    this.setState({
      visible: true,
      teamData,
      showBattery
    });
    this.classList.add('visible');
  }

  hide() {
    this.setState({ visible: false });
    this.classList.remove('visible');
  }

  updateTeam(teamData) {
    this.setState({ teamData });
  }

  styles() {
    return `
      :host {
        display: block;
        position: absolute;
        bottom: 40px;
        left: 40px;
        opacity: 0;
        transform: translateX(-100%);
        transition: all 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
      }

      :host(.visible) {
        opacity: 1;
        transform: translateX(0);
      }

      .team-info-card {
        background: linear-gradient(135deg, rgba(0, 102, 204, 0.95), rgba(0, 51, 153, 0.95));
        border-radius: 15px;
        padding: 25px;
        min-width: 450px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        border: 2px solid rgba(255, 255, 255, 0.2);
      }

      .team-header {
        display: flex;
        align-items: center;
        gap: 20px;
        margin-bottom: 20px;
      }

      .team-photo {
        width: 120px;
        height: 80px;
        border-radius: 8px;
        object-fit: cover;
        border: 2px solid rgba(255, 255, 255, 0.3);
      }

      .team-details {
        flex: 1;
      }

      .team-name {
        font-size: 28px;
        font-weight: bold;
        color: white;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        margin-bottom: 5px;
      }

      .team-university {
        font-size: 16px;
        color: rgba(255, 255, 255, 0.9);
        font-weight: 500;
      }

      .current-battery {
        background: rgba(255, 255, 255, 0.2);
        padding: 8px 15px;
        border-radius: 20px;
        display: inline-block;
        margin-top: 10px;
      }

      .current-battery-label {
        font-size: 14px;
        color: rgba(255, 255, 255, 0.8);
        margin-right: 5px;
      }

      .current-battery-number {
        font-size: 20px;
        font-weight: bold;
        color: white;
      }

      .hidden {
        display: none;
      }
    `;
  }
}

customElements.define('team-info-card', TeamInfoCard);
