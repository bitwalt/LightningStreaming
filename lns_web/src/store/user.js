import localStorage from '../service/local-storage-service'
import axios from 'axios'
import { URLS } from '../constants'

const state = {
    user: {},
    isUserLoggedIn: null,
    token: ""
}

const getters = {
    user: function () {
        return state.user
    },
    isUserLoggedIn: function () {
        return state.isUserLoggedIn
    },
    token: function () {
        return state.token
    },
}

const actions = {
    login(context, user) {
        return axios.post(URLS.api + "auth/login/", {
            username: user.username,
            password: user.password
        })
    },
    register(context, user) {
        return axios.post(URLS.api + "auth/register/", {
            email: user.email,
            username: user.username,
            password: user.password
        })
    },
}

const mutations = {
    initialiseStore() {
        state.isUserLoggedIn = (localStorage.get("userAuthData") != null);

        if (state.isUserLoggedIn) {
            state.user = JSON.parse(localStorage.get("userAuthData"));
            state.token = state.user.token;
        }
    },
    setUser(state, userData) {
        if (typeof userData.token != "undefined" && userData.token != null) {
            var userStorageObject = localStorage.get("userAuthData");

            if (!userStorageObject) {
                userStorageObject = {
                    // id: userData.user.id,
                    token: userData.token,
                    // email: userData.user.email,
                    // first_name: userData.user.first_name,
                    // last_name: userData.user.last_name,
                    // address: userData.user.address,
                    // sex: userData.user.sex,
                    // age: userData.user.age,
                    // terms_agreement: userData.user.terms_agreement,
                    // profile_setup: userData.user.profile_setup,
                    // location: userData.user.location || null,
                    // device: userData.user.device || null,
                };
                localStorage.set("userAuthData", JSON.stringify(userStorageObject));
            }
        }
    },
    logout() {
        console.log("Removing userAuthData from localStorage")
        localStorage.remove("userAuthData");
    }
}

export default {
    namespaced: true,
    state,
    mutations,
    actions,
    getters
}