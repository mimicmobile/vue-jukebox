import Vue from 'vue'
import App from './App.vue'

// import wrap from '@vue/web-component-wrapper'

Vue.config.productionTip = false

new Vue({
  render: h => h(App)
}).$mount('#app')

// const CustomElement = wrap(Vue, App)
// window.customElements.define('juke-box', CustomElement)
