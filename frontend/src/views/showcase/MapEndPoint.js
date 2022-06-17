import axios from 'axios';
import {checkExpire} from '../../services/api';
// import tokenService from "../../services/token.service";
import store from "../../store";


// var token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyaWQiOiJzaXJiYWd1cyIsInR5cGUiOiJQcmVtaXVtIFVzZXIiLCJuYW1lIjoiU2lyIEJhZ3VzIiwiZXhwaXJ5X2RhdGUiOiIyMDIzLTEyLTMwIiwiYWZmaWxpYXRpb24iOiJCaW51cyBVbml2ZXJzaXR5IiwiZXhwIjoxNjU0Nzg0NDIyfQ.DDeQIti9VfAthsFJQ2josALH8OTn6TWkvNO3ioPCul0"
// const headers = {
//   headers: {
//     accept: 'application/json',
//     Authorization: "Bearer " + store.state.auth.user
//   }
// }
// localStorage.getItem("user")
function postDatatoDB(data){
    return axios.post('https://ec2-13-250-37-201.ap-southeast-1.compute.amazonaws.com/api/v1/common/showcase', data, {headers:
    {
      accept: 'application/json',
      Authorization: "Bearer " + store.state.auth.user,
      'Content-Type': 'application/json'
    }
    })
           .then((res) => {
               //Perform Success Action
               
        console.log(res.status);
        return res.status
           })
           .catch((error) => {
              console.log(error.response.data);
              checkExpire(error);
              return [error.response.status,error.response.data]
               // error.response.status Check status code
           }).finally(() => {
             console.log(data)
               //Perform action in always
           });
}

let list =[];
async function getListFieldWell(){
  return axios.get('https://ec2-13-250-37-201.ap-southeast-1.compute.amazonaws.com/api/v1/common/showcase/list-well', {headers:{
    accept: 'application/json',
    Authorization: "Bearer " + store.state.auth.user}
  })
         .then((res) => {
             //Perform Success Action
             
      // console.log(res);
      list = res.data.data;
      console.log(list)
      return list
         })
         .catch((error) => {
            console.log(error.response.data);
            checkExpire(error);


             // error.response.status Check status code
         }).finally(() => {
          //  console.log(data)
             //Perform action in always
         });

}
let dataDB = [];
let allData = [];
let da = [];
function getDatafromDB(){

  return axios.get('https://ec2-13-250-37-201.ap-southeast-1.compute.amazonaws.com/api/v1/common/showcase/list-well', {headers:{
    accept: 'application/json',
    Authorization: "Bearer " + store.state.auth.user}
  })
         .then((res) => {
             //Perform Success Action
             
      da = res.data.data;
      dataDB = da.sort((a, b) => a.fieldName.localeCompare(b.fieldName));

      return dataDB
      // console.log(dataDB)

         })
         .catch((error) => {
          checkExpire(error);

            console.log(error.response.data);

             // error.response.status Check status code
         }).finally(() => {
          //  console.log(data)
             //Perform action in always
         });    
}


function getDB(dat){
  // var allData;
  // let fw = getDatafromDB();
  // let dataFW
  // fw.then(function(result){
  //   dataFW = result
  //   console.log(dataFW)
  var data = {data: dat}
  return axios.post('https://ec2-13-250-37-201.ap-southeast-1.compute.amazonaws.com/api/v1/common/showcase/data', data, {headers:
  {
    accept: 'application/json',
    Authorization: "Bearer " + store.state.auth.user,
    'Content-Type': 'application/json'
  }
  })
         .then((res) => {
             //Perform Success Action
            //  console.log(res.data.data);
             var tempD = res.data.data
             tempD.forEach((o, i) => o.id = i + 1);
             
      allData = tempD;
      return(allData)
         })
         .catch((error) => {
          checkExpire(error);

            console.log(error.response.data);

             // error.response.status Check status code
         }).finally(() => {
             //Perform action in always
         });
        }

  async function restructureData(dataRestructure){
    
    // var t = typeof(dataRestructure)
    // console.log(t)
    var teest = Object.values(dataRestructure)
   
  var fieldIdcheck = []
  var structuredData = []
// console.log(teest)
  for(let x=0;x< teest.length; x++){
    // console.log(teest[x].fieldName)
    if(fieldIdcheck.includes(teest[x].fieldName)){
      var IndexData = structuredData.findIndex((e) => e.name === teest[x].fieldName);
      // console.log(IndexData)
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
  // console.log(structuredData)
  return(structuredData)

  }

  function uploadImages(data){

    return axios.post('https://ec2-13-250-37-201.ap-southeast-1.compute.amazonaws.com/api/v1/common/files', data, {headers:
    {
      accept: 'application/json',
      Authorization: "Bearer " + store.state.auth.user,
      'Content-Type': 'multipart/form-data'
    }
    })
           .then((res) => {
               //Perform Success Action
               console.log(res.status);
              })
              
              .catch((error) => {
                 console.log(error.response.data);
                 checkExpire(error);

                  // error.response.status Check status code
              }).finally(() => {
                  //Perform action in always
              });
  }

  function getImages(pointer){
    return axios.get(`https://ec2-13-250-37-201.ap-southeast-1.compute.amazonaws.com/api/v1/common/files/lists/${pointer}`,{headers:
    {
      accept: 'application/json',
      Authorization: "Bearer " + store.state.auth.user,
    }
    })
           .then((res) => {
               //Perform Success Action
               
        let imagesD = res.data.data;
  
        return imagesD
        // console.log(dataDB)
  
           })
           .catch((error) => {
              console.log(error.response.data);
              checkExpire(error);

               // error.response.status Check status code
           }).finally(() => {
            //  console.log(data)
               //Perform action in always
           });
  }

  function displayImages(imagePath){
    // var data = {path:imagePath}
    // var params = new URLSearchParams([['path', imagePath]]);
    // let imagesArray = []
    // for (let i in imagePath){

    return axios.get(`https://ec2-13-250-37-201.ap-southeast-1.compute.amazonaws.com/api/v1/common/file?path=${encodeURIComponent(imagePath)}`, {
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
// let imagesD = res.data;
// let imagesD = 'data:image/jpeg;base64,' + btoa(images);
// console.log(imagesD)
// console.log(dataDB)

  })
  .catch((error) => {
     console.log(error.response.data);
     checkExpire(error);

      // error.response.status Check status code
  }).finally(() => {
   //  console.log(data)
      //Perform action in always
  });
  }



export{postDatatoDB, getListFieldWell, getDatafromDB, getDB, restructureData, uploadImages, getImages, displayImages}
