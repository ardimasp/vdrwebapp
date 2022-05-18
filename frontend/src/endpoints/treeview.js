import axios from "axios";
import store from "../store";

var userId = store.state.user.id;

var optionAxios = {
    headers: {
        'Content-Type': 'application/json'
    }
}

export const fetchFiles = async () => {
    console.log("id", userId);
    await axios
        .get(`http://ec2-13-250-37-201.ap-southeast-1.compute.amazonaws.com/api/v1/common/files/${userId}/lists`, optionAxios)
        .then(
            (res) => {
                return res;
            },
            (err) => {
                return err;
            }
        )
}