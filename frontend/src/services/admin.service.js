import axios from "axios"
import {URL, checkExpire} from './api'
import store from "../store"

const url = URL + "/registration"
// const headers = {
//     headers: {
//         Authorization: "Bearer " + store.state.auth.user
//     }
// }

class AdminService{
    fetchUsers() {
        return axios.get(`${url}/profile`, {
            headers: {
                Authorization: "Bearer " + store.state.auth.user
            }
        })
            .then(
                (res) => {
                    return res.data;
                },
                (err) => {
                    checkExpire(err);
                    return err.response;
                }
            )
    }
    addUser(data) {
        return axios.post(`${url}/profile`, data, {
            headers: {
                Authorization: "Bearer " + store.state.auth.user
            }
        })
            .then(
                (res) => {
                    return res.status
                },
                (err) => {
                    checkExpire(err);
                    return err.response.status
                }
            )
    }
    editUser(data) {
        return axios.put(`${url}/profile`, data, {
            headers: {
                Authorization: "Bearer " + store.state.auth.user
            }
        })
        .then(
            (res)=> {
                return res.status;
            },
            (err) => {
                checkExpire(err);
                return err.response.status
            }
        )
    }
    deleteUser(data) {
        return axios.delete(`${url}/profile/${data}`, {
            headers: {
                Authorization: "Bearer " + store.state.auth.user
            }
        })
            .then(
                (res) => {
                    return res.status
                },
                (err) => {
                    checkExpire(err);
                    return err.status;
                }
            )
    }
    getUserDetail(data) {
        return axios.get(`${url}/profile/${data}`, {
            headers: {
                Authorization: "Bearer " + store.state.auth.user
            }
        })
            .then(
                (res) => {
                    return res;
                },
                (err) => {
                    checkExpire(err);
                    return err;
                }
            )
    }
}

export default new AdminService();