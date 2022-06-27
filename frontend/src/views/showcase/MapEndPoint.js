import axios from 'axios';
import {checkExpire} from '../../services/api';
import store from "../../store";

function postDatatoDB(data){
    return axios.post('https://ec2-52-77-238-72.ap-southeast-1.compute.amazonaws.com/api/v1/common/showcase', data, {headers:
    {
      accept: 'application/json',
      Authorization: "Bearer " + store.state.auth.user,
      'Content-Type': 'application/json'
    }
    })
           .then((res) => {
               //Perform Success Action
               
        return res.status
           })
           .catch((error) => {
              checkExpire(error);
              return [error.response.status,error.response.data]
               // error.response.status Check status code
           }).finally(() => {
               //Perform action in always
           });
}

let list =[];
async function getListFieldWell(){
  return axios.get('https://ec2-52-77-238-72.ap-southeast-1.compute.amazonaws.com/api/v1/common/showcase/list-well', {headers:{
    accept: 'application/json',
    Authorization: "Bearer " + store.state.auth.user}
  })
         .then((res) => {
             //Perform Success Action
             
      list = res.data.data;
      return list
         })
         .catch((error) => {
            checkExpire(error);


             // error.response.status Check status code
         }).finally(() => {
             //Perform action in always
         });

}
let dataDB = [];
let allData = [];
let da = [];
function getDatafromDB(){

  return axios.get('https://ec2-52-77-238-72.ap-southeast-1.compute.amazonaws.com/api/v1/common/showcase/list-well', {headers:{
    accept: 'application/json',
    Authorization: "Bearer " + store.state.auth.user}
  })
         .then((res) => {
             //Perform Success Action
             
      da = res.data.data;
      dataDB = da.sort((a, b) => a.fieldName.localeCompare(b.fieldName));

      return dataDB
         })
         .catch((error) => {
          checkExpire(error);

             // error.response.status Check status code
         }).finally(() => {
             //Perform action in always
         });    
}


function getDB(dat){

  var data = {data: dat}
  return axios.post('https://ec2-52-77-238-72.ap-southeast-1.compute.amazonaws.com/api/v1/common/showcase/data', data, {headers:
  {
    accept: 'application/json',
    Authorization: "Bearer " + store.state.auth.user,
    'Content-Type': 'application/json'
  }
  })
         .then((res) => {
             //Perform Success Action
             var tempD = res.data.data
             tempD.forEach((o, i) => o.id = i + 1);
             
      allData = tempD;
      return(allData)
         })
         .catch((error) => {
          checkExpire(error);

             // error.response.status Check status code
         }).finally(() => {
             //Perform action in always
         });
        }

  async function restructureData(dataRestructure){
    var teest = Object.values(dataRestructure)
   
  var fieldIdcheck = []
  var structuredData = []
  for(let x=0;x< teest.length; x++){
    if(fieldIdcheck.includes(teest[x].fieldName)){
      var IndexData = structuredData.findIndex((e) => e.name === teest[x].fieldName);
      structuredData[IndexData].children.push({
        name:teest[x].wellName,
        area:teest[x].wellArea,
        latitude:teest[x].wellLatitude,
        longitude:teest[x].wellLongitude,
        oilVolume:teest[x].wellOilVolume,
        gasVolume:teest[x].wellGasVolume,
        waterDepth:teest[x].wellWaterDepth,
        reservoir:teest[x].wellReservoir,
        sourceRock:teest[x].wellSourceRock,
        play:teest[x].wellPlay})
    }
    else{
      fieldIdcheck.push(teest[x].fieldName)
      structuredData.push({name:teest[x].fieldName, children:[{
        name:teest[x].wellName,
        area:teest[x].wellArea,
        latitude:teest[x].wellLatitude,
        longitude:teest[x].wellLongitude,
        oilVolume:teest[x].wellOilVolume,
        gasVolume:teest[x].wellGasVolume,
        waterDepth:teest[x].wellWaterDepth,
        reservoir:teest[x].wellReservoir,
        sourceRock:teest[x].wellSourceRock,
        play:teest[x].wellPlay}]})
    }
  
  }
  return(structuredData)

  }

  function uploadImages(data){

    return axios.post('https://ec2-52-77-238-72.ap-southeast-1.compute.amazonaws.com/api/v1/common/files', data, {headers:
    {
      accept: 'application/json',
      Authorization: "Bearer " + store.state.auth.user,
      'Content-Type': 'multipart/form-data'
    }
    })
           .then((res) => {
             return res.status
               //Perform Success Action
              })
              
              .catch((error) => {
                 checkExpire(error);

                  // error.response.status Check status code
              }).finally(() => {
                  //Perform action in always
              });
  }

  function getImages(pointer){
    return axios.get(`https://ec2-52-77-238-72.ap-southeast-1.compute.amazonaws.com/api/v1/common/files/lists/${pointer}`,{headers:
    {
      accept: 'application/json',
      Authorization: "Bearer " + store.state.auth.user,
    }
    })
           .then((res) => {
               //Perform Success Action
               
        let imagesD = res.data.data;
  
        return imagesD
  
           })
           .catch((error) => {
              checkExpire(error);

               // error.response.status Check status code
           }).finally(() => {
               //Perform action in always
           });
  }

  function displayImages(imagePath){

    return axios.get(`https://ec2-52-77-238-72.ap-southeast-1.compute.amazonaws.com/api/v1/common/file?path=${encodeURIComponent(imagePath)}`, {
    responseType: 'blob', headers:
      {
        accept: 'application/json',
        Authorization: "Bearer " + store.state.auth.user,
      }
      })
    .then((res) => {
      //Perform Success Action
      let imagesD = URL.createObjectURL(res.data)
      return imagesD      
  })
  .catch((error) => {
     checkExpire(error);

      // error.response.status Check status code
  }).finally(() => {
      //Perform action in always
  });
  }

  function vtpUpload(data){
    return axios.post('https://ec2-52-77-238-72.ap-southeast-1.compute.amazonaws.com/api/v1/common/vtpviewer', data, {headers:
    {
      accept: 'application/json',
      Authorization: "Bearer " + store.state.auth.user,
      'Content-Type': 'multipart/form-data'
    }
    })
           .then((res) => {
             return res.status
               //Perform Success Action
              })
              
              .catch((error) => {
                 checkExpire(error);

                  // error.response.status Check status code
              }).finally(() => {
                  //Perform action in always
              });
  }

function vtpInfo(data){
  return axios.post('https://ec2-52-77-238-72.ap-southeast-1.compute.amazonaws.com/api/v1/common/vtpviewer/info', data, {headers:
  {
    accept: 'application/json',
    Authorization: "Bearer " + store.state.auth.user,
    'Content-Type': 'application/json'
  }
  })
         .then((res) => {
             //Perform Success Action
             
      return res.status
         })
         .catch((error) => {
            checkExpire(error);
            return [error.response.status,error.response.data]
             // error.response.status Check status code
         }).finally(() => {
             //Perform action in always
         });
}

function getVTPdata(){
  return axios.get('https://ec2-52-77-238-72.ap-southeast-1.compute.amazonaws.com/api/v1/common/files/lists/?pointers=well-vtp&pointers=line-vtp&pointers=surface-vtp&pathname=true',{headers:
    {
      accept: 'application/json',
      Authorization: "Bearer " + store.state.auth.user,
    }
    })
           .then((res) => {
               //Perform Success Action
               
        let vtpD = res.data.data;
  
        return vtpD
  
           })
           .catch((error) => {
              checkExpire(error);

               // error.response.status Check status code
           }).finally(() => {
               //Perform action in always
           });
}

function getVTPinfo(vtppath){
  var data = {'path': vtppath}
  return axios.post('https://ec2-52-77-238-72.ap-southeast-1.compute.amazonaws.com/api/v1/common/vtpviewer/getInfo', data, {headers:
  {
    accept: 'application/json',
    Authorization: "Bearer " + store.state.auth.user,
    'Content-Type': 'application/json'
  }
    })
           .then((res) => {
               //Perform Success Action
        let vtpInfo = res.data.result;
  
        return vtpInfo
  
           })
           .catch((error) => {
             
              checkExpire(error);

               // error.response.status Check status code
           }).finally(() => {
               //Perform action in always
           });
  }


export{postDatatoDB, getListFieldWell, getDatafromDB, getDB, restructureData, uploadImages, getImages, displayImages, vtpUpload, vtpInfo, getVTPdata, getVTPinfo}
