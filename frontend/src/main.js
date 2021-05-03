import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import axios from "axios";
import { library } from '@fortawesome/fontawesome-svg-core'
import { faPalette } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faPalette)

Vue.component('font-awesome-icon', FontAwesomeIcon)

Vue.prototype.$http = axios;

Vue.config.productionTip = false;

new Vue({
  router,
  render: (h) => h(App),
}).$mount("#app");
