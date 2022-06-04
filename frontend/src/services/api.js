import axios from 'axios'
import store from './../store'
import router from './../router'

export const URL = "https://ec2-13-250-37-201.ap-southeast-1.compute.amazonaws.com/api/v1";

export const checkExpire = (err) => {
    if(err.response && err.response.status == 403 || err.response.status == 401){
        store.dispatch('logout');
        router.push('/login');
    }
    if(store.state.auth.permission == "Administrator" && err.response.status == 500){
        router.push('/admin')
    }
}

const instance = axios.create({
    baseURL: URL,
    headers: {
        'Content-type': 'aplication/json'
    }
})

export default instance;