angular.module("data-service", [])

.factory("dataService", ["$http", function($http) {
	
    var urlBase="/rest";
    var dataService = {};

	// get data
    dataService.getData = function(endpoint, id) {
        
        var apiUrl = urlBase + "/" + endpoint;
        
        // check id
        if (id != null) {
            
            apiUrl += "/" + id;
            
        };
            
        // call data
        return $http.get(apiUrl).then(function(data) {
            
            // return data
            return data.data;
            
        });
		
    };
    
    return dataService;

}]);