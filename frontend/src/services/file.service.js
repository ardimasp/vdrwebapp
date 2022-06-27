import axios from "axios";
import store from "../store";
import {URL, checkExpire} from './api'

const url = URL + "/common"
// const headers = {
//     headers: {
//         Authorization: "Bearer " + store.state.auth.user
//     }
// }

class FileService{
    fetchFiles() {
        return axios.get(`${url}/files/lists`, {
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
    deleteFile(data) {
        return axios.delete(`${url}/files`, 
        {headers: {
            Authorization: "Bearer " + store.state.auth.user
        }, data:{"paths": data}})
            .then(
                (res) => {
                    return res.status;
                },
                (err) => {
                    checkExpire(err);
                    return err.response.status;
                }
            )
    }
    addFile(data){
        return axios.post(`${url}/files`, data, {
            headers: {
                Authorization: "Bearer " + store.state.auth.user
            }
        })
            .then(
                (res) => {
                    return res.status;
                },
                (err) => {
                    checkExpire(err);
                    return err.response.status;
                }
            )
    }
    addFolder(data){
        return axios.post(`${url}/folders`, data, {
            headers: {
                Authorization: "Bearer " + store.state.auth.user
            }
        })
            .then(
                (res) => {
                    return res.status;
                },
                (err) => {
                    checkExpire(err);
                    return err;
                }
            )
    }
    deleteFolder(data){
        return axios.delete(`${url}/folders`, {
            headers: {
                Authorization: "Bearer " + store.state.auth.user
            }, 
            data:{"paths": [data]}
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
    downloadFile(path){
        return axios.get(`${url}/file?path=`+encodeURIComponent(path), 
            {
                headers: {
                    Authorization: "Bearer " + store.state.auth.user
                },
                responseType: 'arraybuffer'
            }
        )
            .then(
                (res) => {
                    var name = path.split("/").pop();
                    var url = window.URL.createObjectURL(new Blob([res.data]))
                    var link = document.createElement('a');
                    document.body.appendChild(link);
                    link.href = url;
                    link.setAttribute('download', name);
                    link.click();
                    link.remove()
                },
                (err) => {
                    checkExpire(err);
                    return err.response.status
                }
            )
    }
    downloadFiles(data){
        var option = {
            headers: {
                Authorization: "Bearer " + store.state.auth.user
            },
            responseType: 'arraybuffer'
        }
        return axios.post(`${url}/files/bulk`, data, option)
            .then(
                (res) => {
                    var url = window.URL.createObjectURL(new Blob([res.data], {type: "application/zip"}))
                    var link = document.createElement('a');
                    document.body.appendChild(link);
                    link.href = url;
                    link.setAttribute('download', 'vdrfolder.zip');
                    link.click();
                    link.remove()
                    return res.data;
                },
                (err) => {
                    checkExpire(err);
                    return err.response.status
                }
            )
    }
    fetchFilesPointer(data, bool) {
        return axios.get(`${url}/files/lists/${data}?pathname=${bool}`, {
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
                    return err.response.status
                }
            )
    }
    fetchFilesMultiPointer(data, bool) {
        return axios.get(`${url}/files/lists/?${data}&pathname=${bool}`, {
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
                    return err.response.status
                }
            )
    }

    getFileRaw(path){
        return axios.get(`${url}/file?path=`+encodeURIComponent(path), 
            {
                headers: {
                    Authorization: "Bearer " + store.state.auth.user
                },
                responseType: 'blob'
            }
        )
            .then(
                (res) => {
                    return res
                },
                (err) => {
                    checkExpire(err);
                    return err.response.status
                }
            )
    }
}

export default new FileService();