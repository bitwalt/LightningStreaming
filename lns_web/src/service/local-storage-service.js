import Vue from 'vue'
import VueLocalStorage from 'vue-localstorage'

Vue.use(VueLocalStorage, {
    name: 'localStorage',
    bind: true, //created computed members from variable declarations
    localStorage: {
        userAuthData: null
    }
});

export default Vue.localStorage;