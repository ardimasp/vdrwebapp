import axios from "axios";
import {URL} from './api';
import tokenService from "./token.service";

const url = URL + "/common"

class AuthService{
    login(data) {
        return axios.post(`${url}/token`, data)
            .then(
                (res) => {
                    let token = res.data.access_token;
                    tokenService.setUser(token);
                    // localStorage.setItem("username", res.data.name);
                    localStorage.setItem("type", res.data.type);
                    console.log("successful login", localStorage.getItem("user"));
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