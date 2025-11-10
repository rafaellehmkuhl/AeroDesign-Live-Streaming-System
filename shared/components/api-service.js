class ApiService extends HTMLElement {
  constructor() {
    super();
    this.apiBase = 'http://localhost:8000/api';
    this.pollInterval = null;
    this.pollRate = 500;
  }

  connectedCallback() {
    window.aeroApi = {
      getTeams: () => this.getTeams(),
      getTeam: (id) => this.getTeam(id),
      getOverlayState: () => this.getOverlayState(),
      updateOverlayState: (state) => this.updateOverlayState(state),
      showOverlay: (teamId) => this.showOverlay(teamId),
      hideOverlay: () => this.hideOverlay(),
      toggleOverlay: () => this.toggleOverlay(),
      updateTeam: (teamId, data) => this.updateTeam(teamId, data),
      updateCurrentBattery: (teamId, batteryNumber) => this.updateCurrentBattery(teamId, batteryNumber),
      addFlightResult: (teamId, result) => this.addFlightResult(teamId, result)
    };

    if (this.hasAttribute('auto-poll')) {
      this.startPolling();
    }
  }

  disconnectedCallback() {
    this.stopPolling();
  }

  startPolling() {
    if (this.pollInterval) return;

    this.pollInterval = setInterval(async () => {
      try {
        const state = await this.getOverlayState();
        this.dispatchEvent(new CustomEvent('state-updated', {
          detail: state,
          bubbles: true,
          composed: true
        }));
      } catch (error) {
        console.error('Polling error:', error);
      }
    }, this.pollRate);

    this.getOverlayState().then(state => {
      this.dispatchEvent(new CustomEvent('state-updated', {
        detail: state,
        bubbles: true,
        composed: true
      }));
    });
  }

  stopPolling() {
    if (this.pollInterval) {
      clearInterval(this.pollInterval);
      this.pollInterval = null;
    }
  }

  async getTeams() {
    const response = await fetch(`${this.apiBase}/teams`);
    if (!response.ok) throw new Error('Failed to fetch teams');
    return await response.json();
  }

  async getTeam(teamId) {
    const response = await fetch(`${this.apiBase}/teams/${teamId}`);
    if (!response.ok) throw new Error('Failed to fetch team');
    return await response.json();
  }

  async getOverlayState() {
    const response = await fetch(`${this.apiBase}/overlay/state`);
    if (!response.ok) throw new Error('Failed to fetch overlay state');
    return await response.json();
  }

  async updateOverlayState(state) {
    const response = await fetch(`${this.apiBase}/overlay/state`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(state)
    });
    if (!response.ok) throw new Error('Failed to update overlay state');
    return await response.json();
  }

  async showOverlay(teamId = null) {
    const url = teamId
      ? `${this.apiBase}/overlay/show?team_id=${teamId}`
      : `${this.apiBase}/overlay/show`;

    const response = await fetch(url, { method: 'POST' });
    if (!response.ok) throw new Error('Failed to show overlay');
    return await response.json();
  }

  async hideOverlay() {
    const response = await fetch(`${this.apiBase}/overlay/hide`, { method: 'POST' });
    if (!response.ok) throw new Error('Failed to hide overlay');
    return await response.json();
  }

  async toggleOverlay() {
    const response = await fetch(`${this.apiBase}/overlay/toggle`, { method: 'POST' });
    if (!response.ok) throw new Error('Failed to toggle overlay');
    return await response.json();
  }

  async updateTeam(teamId, teamData) {
    const response = await fetch(`${this.apiBase}/teams/${teamId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(teamData)
    });
    if (!response.ok) throw new Error('Failed to update team');
    return await response.json();
  }

  async updateCurrentBattery(teamId, batteryNumber) {
    const response = await fetch(`${this.apiBase}/teams/${teamId}/battery?battery_number=${batteryNumber}`, {
      method: 'PUT'
    });
    if (!response.ok) throw new Error('Failed to update battery');
    return await response.json();
  }

  async addFlightResult(teamId, result) {
    const response = await fetch(`${this.apiBase}/teams/${teamId}/results`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(result)
    });
    if (!response.ok) throw new Error('Failed to add flight result');
    return await response.json();
  }
}

customElements.define('api-service', ApiService);
