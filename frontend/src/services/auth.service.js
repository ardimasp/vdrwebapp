import axios from "axios";
import { decode, } from "../function";
import {URL} from './api';
import tokenService from "./token.service";

const url = URL + "/common"

class AuthService{
    login(data) {
        return axios.post(`${url}/token`, data)
            .then(
                (res) => {
                    let token = res.data.access_token;
                    localStorage.setItem("string", decode(token).exp)
                    tokenService.setUser(token);
                    // console.log("successful login", localStorage.getItem("user"));
                    return res;
                },
                (err) => {
                    console.log(err);
                    return err.response;
                }
            )
    }
    logout(){
        tokenService.removeUser();
    }
}

export default new AuthService();