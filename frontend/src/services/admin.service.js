import axios from "axios"
import {URL, checkExpire} from './api'
import store from "../store"
// import tokenService from "./token.service"

const url = URL + "/registration"
// const headers = {
//     headers: {
//         Authorization: "Bearer " + localStorage.getItem("user")
//     }
// }

class AdminService{
    fetchUsers() {
        return axios.get(`${url}/profile`, {
            headers: {
                Authorization: "Bearer " + localStorage.getItem("user")
            }
        })
            .then(
                (res) => {
                    console.log("success fetch users", res.data)
                    return res.data;
                },
                (err) => {
                    console.log(err);
                    checkExpire(err);
                    return err.response;
                }
            )
    }
    addUser(data) {
        // console.log("aaaa",localStorage.getItem("user"));
        return axios.post(`${url}/profile`, data, {
            headers: {
                Authorization: "Bearer " + store.state.auth.user
            }
        })
            .then(
                (res) => {
                    console.log(res)
                    return res.status
                },
                (err) => {
                    console.log(err);
                    checkExpire(err);
                    return err.response.status
                }
            )
    }
    editUser(data) {
        return axios.put(`${url}/profile`, data, {
            headers: {
                Authorization: "Bearer " + localStorage.getItem("user")
            }
        })
        .then(
            (res)=> {
                console.log(res);
                return res.status;
            },
            (err) => {
                console.log(err);
                checkExpire(err);
                return err.response.status
            }
        )
    }
    deleteUser(data) {
        return axios.delete(`${url}/profile/${data}`, {
            headers: {
                Authorization: "Bearer " + localStorage.getItem("user")
            }
        })
            .then(
                (res) => {
                    console.log(res);
                    return res.status
                },
                (err) => {
                    console.log(err);
                    checkExpire(err);
                    return err.status;
                }
            )
    }
    getUserDetail(data) {
        return axios.get(`${url}/profile/${data}`, {
            headers: {
                Authorization: "Bearer " + localStorage.getItem("user")
            }
        })
            .then(
                (res) => {
                    console.log(res);
                    return res;
                },
                (err) => {
                    console.log(err);
                    checkExpire(err);
                    return err;
                }
            )
    }
}

export default new AdminService();