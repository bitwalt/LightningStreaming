import axios from 'axios';
import userStore from '../store/user'
import store from '../store'
import router from '../routes'

export default function setup() {
    axios.interceptors.request.use(function (config) {
        // SET TOKEN
        const token = userStore.state.token;
        if (token) {
            config.headers.Authorization = `JWT ${token}`;
        }
        return config;
    }, function (err) {
        return Promise.reject(err);
    });

    axios.interceptors.response.use(function (response) {
        return response;
    }, function (err) {
        if (err.message.includes("401")) {
            store.commit("userModule/logout");
            router.go("/");
            return;
        }
        // Do something with response error
        return Promise.reject(err);
    });
}