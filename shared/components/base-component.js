class BaseComponent extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this._state = {};
    this._eventListeners = [];
  }

  setState(newState) {
    const oldState = { ...this._state };
    this._state = { ...this._state, ...newState };
    this.onStateChange(oldState, this._state);
    this.render();
  }

  getState() {
    return { ...this._state };
  }

  onStateChange(oldState, newState) {}

  template() {
    return '';
  }

  styles() {
    return '';
  }

  render() {
    this.shadowRoot.innerHTML = `
      <style>${this.styles()}</style>
      ${this.template()}
    `;
    this.afterRender();
  }

  afterRender() {}

  $(selector) {
    return this.shadowRoot.querySelector(selector);
  }

  $$(selector) {
    return this.shadowRoot.querySelectorAll(selector);
  }

  addManagedListener(element, event, handler) {
    element.addEventListener(event, handler);
    this._eventListeners.push({ element, event, handler });
  }

  removeAllEventListeners() {
    this._eventListeners.forEach(({ element, event, handler }) => {
      element.removeEventListener(event, handler);
    });
    this._eventListeners = [];
  }

  disconnectedCallback() {
    this.removeAllEventListeners();
  }

  emit(eventName, detail = {}) {
    this.dispatchEvent(new CustomEvent(eventName, {
      detail,
      bubbles: true,
      composed: true
    }));
  }
}

window.BaseComponent = BaseComponent;
