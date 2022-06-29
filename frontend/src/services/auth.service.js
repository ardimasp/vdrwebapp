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
                    return res;
                },
                (err) => {
                    return err;
                }
            )
    }
    logout(){
        tokenService.removeUser();
    }
}

export default new AuthService();