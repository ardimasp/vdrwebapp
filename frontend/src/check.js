import axios from "axios";
import store from "./store";
// import route from './router';

const urlAPI = store.state.url;
const userId = store.state.user.id;

var optionAxios = {
    headers: {
        Authorization: "Bearer " + userId,
    }
}
export const checkToken = async () => {
    console.log("hello")
    let bool = false;
    await axios.get(`${urlAPI}/test`, optionAxios)
        .then(
            (res) => {
                bool = true;
                console.log("success", res.data)
                // return bool;
                // return res.data
            },
            (err) => {
                bool = false;
                // route.push('/login');
                return err;
            }
        )
    return bool;
}