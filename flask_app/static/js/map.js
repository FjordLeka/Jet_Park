let map;

function initMap() {
  var location1 = { lat: 41.41927, lng: 19.71333 };  // Location 1 coordinates
  var location2 = { lat: 40.46698, lng: 19.48977 };  // Location 2 coordinates
  var location3 = { lat: 42.03651, lng: 20.41804 };    // Location 3 coordinates

  var map = new google.maps.Map(document.getElementById('map'), {
    center: location1,  // Set the map's center to Location 1
    zoom: 6.5           // Adjust the zoom level as needed
  });

  // Add markers for each location
  var marker1 = new google.maps.Marker({ position: location1, map: map });
  var marker2 = new google.maps.Marker({ position: location2, map: map });
  var marker3 = new google.maps.Marker({ position: location3, map: map });
}

initMap();