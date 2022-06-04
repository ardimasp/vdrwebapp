import axios from "axios";
import {URL, checkExpire} from './api'
import tokenService from "./token.service";

const url = URL + "/common"
const headers = {
    headers: {
        Authorization: "Bearer " + tokenService.getLocalAccessToken()
    }
}

class FileService{
    fetchFiles() {
        return axios.get(`${url}/files/lists`, {
            headers: {
                Authorization: "Bearer " + localStorage.getItem("user")
            }
        })
            .then(
                (res) => {
                    console.log("success fetch", res.data);
                    return res.data;
                },
                (err) => {
                    console.log("error fetch", err);
                    checkExpire(err);
                    return err.response;
                }
            )
    }
    deleteFile(data) {
        return axios.delete(`${url}/files`, 
        {headers: {
            Authorization: "Bearer " + tokenService.getLocalAccessToken()
        }, data:{"paths": data}})
            .then(
                (res) => {
                    console.log(res.status);
                    return res.status;
                },
                (err) => {
                    console.log(err)
                    checkExpire(err);
                    return err.response.status;
                }
            )
    }
    addFile(data){
        return axios.post(`${url}/files`, data, headers)
            .then(
                (res) => {
                    return res.status;
                },
                (err) => {
                    console.log(err);
                    checkExpire(err);
                    return err.response.status;
                }
            )
    }
    addFolder(data){
        return axios.post(`${url}/folders`, data, headers)
            .then(
                (res) => {
                    console.log(res);
                    return res.status;
                },
                (err) => {
                    console.log(err);
                    checkExpire(err);
                    return err;
                }
            )
    }
    deleteFolder(data){
        return axios.delete(`${url}/folders`, {
            headers: {
                Authorization: "Bearer " + tokenService.getLocalAccessToken()
            }, 
            data:{"paths": [data]}
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
    downloadFile(path){
        var url = `${url}/file?path=`+path;
        var link = document.createElement("a");
        link.href = encodeURI(url);
        link.target = "_blank";
        link.click();
    }
    downloadFiles(data){
        var option = {
            headers: {
                Authorization: "Bearer " + tokenService.getLocalAccessToken()
            },
            responseType: 'arraybuffer'
        }
        return axios.post(`${url}/files/bulk`, data, option)
            .then(
                (res) => {
                    console.log("check bulk download", res.data);
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
                    console.log(err)
                    checkExpire(err);
                    return err.response.status
                }
            )
    }
}

export default new FileService();