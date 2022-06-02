import axios from 'axios';


var token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyaWQiOiJzaXJiYWd1cyIsInR5cGUiOiJQcmVtaXVtIFVzZXIiLCJuYW1lIjoiU2lyIEJhZ3VzIiwiZXhwaXJ5X2RhdGUiOiIyMDIzLTEyLTMwIiwiYWZmaWxpYXRpb24iOiJCaW51cyBVbml2ZXJzaXR5IiwiZXhwIjoxNjU0MTc2Mjg5fQ.fi3Uw2FgBOnSut_shLD1GpL6lwmTEw3DYE7atge2uYM"
function postDatatoDB(data){
    axios.post('https://ec2-13-250-37-201.ap-southeast-1.compute.amazonaws.com/api/v1/common/showcase', data, {headers:
    {
      accept: 'application/json',
      Authorization: "Bearer " + token,
      'Content-Type': 'application/json'
    }
    })
           .then((res) => {
               //Perform Success Action
               
        console.log(res.status);
           })
           .catch((error) => {
              console.log(error.response.data);

               // error.response.status Check status code
           }).finally(() => {
             console.log(data)
               //Perform action in always
           });
}
// const getTodoItems = async () => {
//   try {
//     const response = await axios.get('https://ec2-13-250-37-201.ap-southeast-1.compute.amazonaws.com/api/v1/common/showcase/list-well', {headers:
//     {
//       accept: 'application/json',
//       Authorization: "Bearer " + token,
//     }
//     })

//     const todoItems = response.data.data;

//     console.log(`GET: Here's the list of todos`, todoItems);

//     return todoItems;
//   } catch (errors) {
//     console.error(errors);
//   }
// };
let list =[];
async function getListFieldWell(){
  return axios.get('https://ec2-13-250-37-201.ap-southeast-1.compute.amazonaws.com/api/v1/common/showcase/list-well', {headers:
  {
    accept: 'application/json',
    Authorization: "Bearer " + token,
  }
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

  return axios.get('https://ec2-13-250-37-201.ap-southeast-1.compute.amazonaws.com/api/v1/common/showcase/list-well', {headers:
  {
    accept: 'application/json',
    Authorization: "Bearer " + token,
  }
  })
         .then((res) => {
             //Perform Success Action
             
      da = res.data.data;
      dataDB = da.sort((a, b) => a.fieldName.localeCompare(b.fieldName));

      return dataDB
      // console.log(dataDB)

         })
         .catch((error) => {
            console.log(error.response.data);

             // error.response.status Check status code
         }).finally(() => {
          //  console.log(data)
             //Perform action in always
         });
//          axios.post('https://ec2-13-250-37-201.ap-southeast-1.compute.amazonaws.com/api/v1/common/showcase/data', dataDB, {headers:
//          {
//            accept: 'application/json',
//            Authorization: "Bearer " + token,
//            'Content-Type': 'application/json'
//          }
//          })
//                 .then((res) => {
//                     //Perform Success Action
                    
//              allData = res.data;
//                 })
//                 .catch((error) => {
//                    console.log(error.response.data);
       
//                     // error.response.status Check status code
//                 }).finally(() => {
//                   console.log('s')
//                     //Perform action in always
//                 });
// console.log(allData)
// return(allData)

        
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
    Authorization: "Bearer " + token,
    'Content-Type': 'application/json'
  }
  })
         .then((res) => {
             //Perform Success Action
             console.log(res.data.data);
             var tempD = res.data.data
             tempD.forEach((o, i) => o.id = i + 1);

            //  var prev = res.data.data.fieldName
            //   var ind = 1
            //   res.data.data.id = ind
            //  for (let x=1; x < res.data.data.length; x++){
            //   if(prev === res.data.data[x].fieldName){
            //     res.data.data[x].id = ind
            //   }else{
            //     ind = ind + 1
            //     res.data.data[x].id = ind
            //   }
            //  }

             
      allData = tempD;
      return(allData)
         })
         .catch((error) => {
            console.log(error.response.data);

             // error.response.status Check status code
         }).finally(() => {
             //Perform action in always
         });
        }

  async function restructureData(dataRestructure){
    
    var t = typeof(dataRestructure)
    console.log(t)
    var teest = Object.values(dataRestructure)
   
  var fieldIdcheck = []
  var structuredData = []
console.log(teest)
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
      Authorization: "Bearer " + token,
      'Content-Type': 'multipart/form-data'
    }
    })
           .then((res) => {
               //Perform Success Action
               console.log(res.status);
              })
              
              .catch((error) => {
                 console.log(error.response.data);
     
                  // error.response.status Check status code
              }).finally(() => {
                  //Perform action in always
              });
  }
  // return axios.post('https://ec2-13-250-37-201.ap-southeast-1.compute.amazonaws.com/api/v1/common/showcase/data', dataFW, {headers:
  // {
  //   accept: 'application/json',
  //   Authorization: "Bearer " + token,
  //   'Content-Type': 'application/json'
  // }
  // })
  //        .then((res) => {
  //            //Perform Success Action
             
  //     console.log(res.data);
  //     allData = res.data;
  //     return(allData)
  //        })
  //        .catch((error) => {
  //           console.log(error.response.data);

  //            // error.response.status Check status code
  //        }).finally(() => {
  //          console.log('s')
  //            //Perform action in always
  //        });


export{postDatatoDB, getListFieldWell, getDatafromDB, getDB, restructureData, uploadImages}