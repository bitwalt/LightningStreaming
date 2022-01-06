import Vue from 'vue'
import Vuex from 'vuex'
import userModule from './user'

Vue.use(Vuex);

const store = new Vuex.Store({
    modules: {
        userModule,
    }
});

store.commit("userModule/initialiseStore");

export default store;