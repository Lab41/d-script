angular.module("data-service", [])

.factory("dataService", ["$http", function($http) {
	
    var urlBase="/rest";
    var dataService = {};

	// get data
    dataService.getData = function(endpoint, id) {
        
        // api call for a specific viz data set
        var apiUrl = urlBase + "/" + endpoint + "/" + id;
            
        // call data
        return $http.get(apiUrl).then(function(data) {
            
            // return data
            return data.data;
            
        });
		
    };
    
    return dataService;

}]);