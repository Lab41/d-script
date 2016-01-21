angular.module("map-directive", [])

.directive("map", ["mapService", function(mapService) {
	return {
		restrict: "A",
        scope: {
            geojson: "="
        },
		link: function(scope, element, attrs) {
            
            var map = L.map(element[0]);
                                           
            // bind data
            scope.$watch("geojson", function(newData, oldData) {
                
                // async check
                if (newData !== undefined && newData.features.length > 0) {
                    
                    function draw(data) {
                        
                        // remove layers before adding more
                        map.eachLayer(function(layer) {
                            map.removeLayer(layer);
                        });
                                                
                        // new marker group
                        var markers = L.markerClusterGroup();
                        
                        // bind data to marker clusters
                        var geoJsonLayer = L.geoJson(data, {

                            // add labels
                            onEachFeature: function (feature, layer) {

                                // set popup options
                                var popUpOptions = {
                                    autoPan: false,
                                    maxHeight: 200,
                                    maxWidth: 300,
                                    offset: L.point(0, -10)
                                };

                                // custom popup content
                                var label = "<h3>" + feature.properties.name + "</h3>";

                                layer.bindPopup(label, popUpOptions);

                            },

                            // add style
                            style: function(feature) {
                                switch (feature.properties.name) {
                                    case "physical": return { color: "#c8de4d" };
                                    case "virtual": return { color: "#ff4500" };
                                    default: return { color: "#009dff" };
                                }
                            },

                            // add circle marker
                            pointToLayer: function(feature, latlng) {
                                switch (feature.properties.name) {
                                    case "up": return L.marker(latlng, { icon: L.divIcon(mapService.up) });
                                    default: return L.marker(latlng, { icon: L.divIcon(mapService.up) });
                                }
                            }

                        });

                        // bind markers to layer
                        markers.addLayer(geoJsonLayer);
                        
                        // add control
                        //map.addControl(L.mapbox.geocoderControl("mapbox.places", { autocomplete: true }));

                        // add tiles to map
                        L.tileLayer('https://{s}.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', mapService.tiles).addTo(map);

                        // add marker clusters to map
                        map.addLayer(markers);

                        // get bounds
                        var ne = [geoJsonLayer.getBounds()["_northEast"].lat, geoJsonLayer.getBounds()["_northEast"].lng];
                        var sw = [geoJsonLayer.getBounds()["_southWest"].lat, geoJsonLayer.getBounds()["_southWest"].lat];

                        // center and zoom map based on markers
                        map.fitBounds([sw, ne]);
                       
                    };
                    
                    // check new vs old
                    var isMatching = angular.equals(newData, oldData);
                    
                    // if false
                    if (!isMatching) {
                        
                        // update the viz
                        draw(newData);
                        
                    };
                    
                };
                
            });
			
		}
		
	};
	
}]);