import axios from "axios";
import {URL, checkExpire} from './api'
import store from "../store";

const url = URL + "/prediction"
// const headers = {
//     headers: {
//         Authorization: "Bearer " + store.state.auth.user
//     }
// }

class SreeyaService{
    oilPrediction(data){
        return axios.post(`${url}/oil-production`, data, {
            headers: {
                Authorization: "Bearer " + store.state.auth.user
            }
        })
            .then(
                (res) => {
                    return res.data
                },
                (err) => {
                    console.log(err)
                    checkExpire(err);
                    return err.response.status
                }
            )
    }
    gasPrediction(data){
        return axios.post(`${url}/gas-production`, data, {
            headers: {
                Authorization: "Bearer " + store.state.auth.user
            }
        })
            .then(
                (res) => {
                    return res.data
                },
                (err) => {
                    console.log(err)
                    checkExpire(err);
                    return err.response.status
                }
            )
    }
    oilPredictionExcel(data){
        return axios.post(`${url}/oil-production-excel?path=`+encodeURIComponent(data), '', {
            headers: {
                Authorization: "Bearer " + store.state.auth.user
            },
        })
            .then(
                (res) => {
                    return res.data
                },
                (err) => {
                    console.log(err)
                    checkExpire(err);
                    return err.response.status
                }
            )
    }
    gasPredictionExcel(data){
        return axios.post(`${url}/gas-production-excel?path=`+encodeURIComponent(data), '', {
            headers: {
                Authorization: "Bearer " + store.state.auth.user
            }, 
        })
            .then(
                (res) => {
                    return res.data
                },
                (err) => {
                    console.log(err)
                    checkExpire(err);
                    return err
                }
            )
    }
}

export default new SreeyaService()