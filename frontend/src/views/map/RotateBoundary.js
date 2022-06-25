import 'leaflet/dist/leaflet.css'
import L from 'leaflet'
var map = L.map('map').setView([24, 54], 12);
var mapLink = '<a href="http://openstreetmap.org">OpenStreetMap</a>';
L.tileLayer(
   'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
       attribution: '&copy; ' + mapLink + ' Contributors',
       maxZoom: 18,
       autoPan: true
   }).addTo(map);

   var ExpressLayers = L.layerGroup().addTo(map);

function rectangleLatlng(lat, lng, rad, angles) {
    
    // //clear old layers
    ExpressLayers.clearLayers();
    
    // //create a marker and add to layer group
    // var marker = L.marker([lat,lng], { draggable: 'true', autoPan: true }).addTo(map);
    // ExpressLayers.addLayer(marker);

    // //create a cirle and add to layer group
    var circle = L.circle([lat, lng], { color: "white", fillColor: "#f03", fillOpacity: 0.0, radius: rad }).addTo(map);
    ExpressLayers.addLayer(circle);

    //prepare data for create a square around with defined angle
    var centerpoint = [lat, lng];
    var retpoint = [];
    retpoint =   rotateboundary(centerpoint , circle.getBounds(), angles);
    return(retpoint)
    // //draw polygon from received coordinates
    // var polygon = L.polygon([retpoint], { color: 'green' });
    // polygon.addTo(map);
    // ExpressLayers.addLayer(polygon);
  
  

}


function rotateboundary(CenterPoint, circlebounds, angles) {

    var ne_lat = circlebounds._northEast.lat;
    var ne_lon = circlebounds._northEast.lng;

    var sw_lat = circlebounds._southWest.lat;
    var sw_lon = circlebounds._southWest.lng;
    
    var pointlist = [];   

    var p1 = [sw_lat, ne_lon];
    pointlist.push(p1);
    var p2 = [ne_lat, ne_lon];
    pointlist.push(p2);
    var p3 = [ne_lat, sw_lon];
    pointlist.push(p3);
    var p4 = [sw_lat, sw_lon];
    pointlist.push(p4);    


    
    
    const res = []
    const centerPoint = map.latLngToLayerPoint(CenterPoint)
    const angle = angles * (Math.PI / 180)
            for (let i = 0; i < pointlist.length; i++) {
                    const p = map.latLngToLayerPoint(pointlist[i])
                    // translate to center
                    const p2 = new L.Point(p.x - centerPoint.x, p.y - centerPoint.y)
                    // rotate using matrix rotation
                    const p3 = new L.Point(Math.cos(angle) * p2.x - Math.sin(angle) * p2.y, Math.sin(angle) * p2.x + Math.cos(angle) * p2.y)
                    // translate back to center
                    let p4 = new L.Point(p3.x + centerPoint.x, p3.y + centerPoint.y)
                    // done with that point
                    p4 = map.layerPointToLatLng(p4)
                    res.push(p4)
            }
            
            
    
    
    
return res;

} 

export{rotateboundary, rectangleLatlng}