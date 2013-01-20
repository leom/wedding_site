// Google Map Custom Marker Maker 2012
// Please include the following credit in your code

// Sample custom marker code created with Google Map Custom Marker Maker
// http://powerhut.co.uk/googlemaps/custom_markers.php

var hotelMarkerImg = new google.maps.MarkerImage(
  '/static/img/gmap-markers/hotel.png',
  new google.maps.Size(26,30),
  new google.maps.Point(0,0),
  new google.maps.Point(0,30)
);

var hotelMarkerShadow = new google.maps.MarkerImage(
  '/static/img/gmap-markers/hotel-shadow.png',
  new google.maps.Size(44,30),
  new google.maps.Point(0,0),
  new google.maps.Point(0,30)
);

var hotelMarkerShape = {
  coord: [24,0,25,1,25,2,25,3,25,4,25,5,25,6,25,7,25,8,25,9,25,10,25,11,25,12,25,13,25,14,25,15,25,16,25,17,25,18,25,19,25,20,25,21,25,22,25,23,25,24,24,25,21,26,18,27,17,28,16,29,9,29,8,28,7,27,4,26,1,25,0,24,0,23,0,22,0,21,0,20,0,19,0,18,0,17,0,16,0,15,0,14,0,13,0,12,0,11,0,10,0,9,0,8,0,7,0,6,0,5,0,4,0,3,0,2,0,1,1,0,24,0],
  type: 'poly'
};

var hacMarkerImg = new google.maps.MarkerImage(
  '/static/img/gmap-markers/hac.png',
  new google.maps.Size(35,32),
  new google.maps.Point(0,0),
  new google.maps.Point(0,32)
);

var hacMarkerShadow = new google.maps.MarkerImage(
  '/static/img/gmap-markers/hac-shadow.png',
  new google.maps.Size(55,32),
  new google.maps.Point(0,0),
  new google.maps.Point(0,32)
);

var hacMarkerShape = {
  coord: [30,0,31,1,32,2,33,3,33,4,34,5,34,6,34,7,34,8,34,9,34,10,34,11,34,12,33,13,33,14,32,15,31,16,30,17,28,18,27,19,26,20,25,21,24,22,23,23,22,24,21,25,20,26,20,27,19,28,19,29,18,30,18,31,16,31,16,30,15,29,15,28,14,27,14,26,13,25,12,24,11,23,10,22,9,21,8,20,7,19,6,18,4,17,3,16,2,15,1,14,1,13,0,12,0,11,0,10,0,9,0,8,0,7,0,6,0,5,1,4,1,3,2,2,3,1,4,0,30,0],
  type: 'poly'
};
