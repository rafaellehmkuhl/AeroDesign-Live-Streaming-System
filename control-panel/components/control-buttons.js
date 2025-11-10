class ControlButtons extends BaseComponent {
  template() {
    return `
      <div class="controls">
        <button class="button button-show">✅ Mostrar Overlay</button>
        <button class="button button-hide">❌ Esconder Overlay</button>
        <button class="button button-toggle">🔄 Alternar Overlay</button>
      </div>
    `;
  }

  constructor() {
    super();
  }

  connectedCallback() {
    this.render();
  }

  afterRender() {
    this.$('.button-show').addEventListener('click', () => {
      this.emit('show-overlay');
    });

    this.$('.button-hide').addEventListener('click', () => {
      this.emit('hide-overlay');
    });

    this.$('.button-toggle').addEventListener('click', () => {
      this.emit('toggle-overlay');
    });
  }

  styles() {
    return `
      :host {
        display: block;
      }

      .controls {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 15px;
      }

      .button {
        padding: 12px 24px;
        border: none;
        border-radius: 6px;
        font-size: 16px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s;
        text-align: center;
        font-family: inherit;
      }

      .button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
      }

      .button:active {
        transform: translateY(0);
      }

      .button-show {
        background: #00cc66;
        color: white;
      }

      .button-hide {
        background: #ff4757;
        color: white;
      }

      .button-toggle {
        background: #ffa502;
        color: white;
      }
    `;
  }
}

customElements.define('control-buttons', ControlButtons);
