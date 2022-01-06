import Vue from "vue";
// import localStorage from './service/local-storage-service'
import VueRouter from "vue-router";
import RouterPrefetch from 'vue-router-prefetch'
import App from "./App";
import store from './store/index'

// TIP: change to import router from "./router/starterRouter"; to start with a clean layout
import router from "./router/index";

import BlackDashboard from "./plugins/blackDashboard";
import i18n from "./i18n"
// import './registerServiceWorker'

Vue.use(BlackDashboard);
Vue.use(VueRouter);
Vue.use(RouterPrefetch);

/* eslint-disable no-new */
new Vue({
  // localStorage,
  router,
  store,
  i18n,
  render: h => h(App)
}).$mount("#app");

export {app, store}