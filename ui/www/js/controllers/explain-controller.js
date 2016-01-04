angular.module("explain-controller", [])

.controller("explainCtrl", ["$scope", "dataService", function($scope, dataService) {
    
    /**************************/
    /********* !DATA **********/
    /**************************/
    
    $scope.nodelink;
	$scope.nodelinkcluster;
	$scope.pie;
	$scope.venn;
    
    /****************************/
    /********* !EVENTS **********/
    /****************************/
    
    /*******************************/
    /********* !FUNCTIONS **********/
    /*******************************/
    
    // get data to use in visualizations
    getData("nodelink");
	getData("nodelinkcluster");
	getData("pie");
	getData("venn");
    
    // viz data
	function getData(name) {
		dataService.getData(name).then(function(data) {
                        
            // assign to scope
			$scope[name] = data;
            
		});
		
	};
	
}]);