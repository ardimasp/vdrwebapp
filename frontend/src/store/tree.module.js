import axios from 'axios'

export default {
    state: {
        list: [],
        length: 20,
    },
    mutations: {
        UPDATE_TREE(state, payload){
            state.list = payload;
        },
        UPDATE_LENGTH(state, payload){
            state.length = payload;
        },
    },
    actions: {
        fetchTreeList(context, userId){
            var optionAxios = {
                headers: {
                    'Content-Type': 'application/json'
                }
            }
            return axios
                .get(`http://ec2-13-250-37-201.ap-southeast-1.compute.amazonaws.com/api/v1/common/files/${userId}/lists`, optionAxios)
                .then(
                    (res) => {
                        let callList = res.data;
                        context.commit('UPDATE_TREE', callList.data);
                    },
                    (err) => {
                        console.log(err);
                    }
                )
        }
    }
}