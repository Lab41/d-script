angular.module("explain-controller", [])

.controller("explainCtrl", ["$scope", "dataService", function($scope, dataService) {
    
    /**************************/
    /********* !DATA **********/
    /**************************/
    
    $scope.details = [];
    $scope.features;
    
	$scope.allNodes;
    $scope.nodes;
    $scope.offset = 0; // starting point
    
    /****************************/
    /********* !EVENTS **********/
    /****************************/
    
    // control slider navigation
    $scope.currentIndex = 0;
    
    $scope.setCurrentSlideIndex = function(idx) {
        $scope.currentIndex = idx;
    };
    
    $scope.isCurrentSlideIndex = function(idx) {
        return $scope.currentIndex === idx;
    };
    
    $scope.previous = function() {
        $scope.currentIndex = ($scope.currentIndex < $scope.details.length - 1) ? ++$scope.currentIndex : 0;
    };
    
    $scope.next = function() {
        $scope.currentIndex = ($scope.currentIndex > 0) ? --$scope.currentIndex : $scope.details.length - 1;
    };
    
    // add new node
    $scope.addNode = function(id) {
        
        // add dummy node
        // might be API call?
        var allNodes = $scope.nodes.nodes;
        var links = $scope.nodes.links;
        var newNodes = allNodes.concat({"id": "new"});
        
        var obj = {nodes: newNodes, links: links};
        
        // add to scope to trigger viz change
        $scope.nodes = obj;
        
    };
    
    // add a batch of existing nodes
    // load from API
    $scope.addNodes = function(offset, count) {
        
        // set existing values from current scope
        var nodes = $scope.nodes.nodes;
        var links = $scope.nodes.links;
        
        // set needed variables
        var allNodes = $scope.allNodes.nodes;
        var addNodes = [];
        var offsetAdj = count + offset;
        
        // check that the node request doesn't exceed available nodes
        if (offsetAdj > allNodes.length) {
            
            // set new count for loop
            var nodeCount = allNodes.length - nodes.length;
            
            // disable button
            $scope.isDisabled = true;
            
        } else {
            
            // use adjustment
            var nodeCount = offsetAdj;
            
        }
        
        // loop through available nodes
        for (var i=offset; i < nodeCount; i++) {
            
            // add to data set
            addNodes.push(allNodes[i]);
            
        };
        
        // add new nodes to existing
        var newNodes = nodes.concat(addNodes);
        
        // construct new dataset
        var obj = { nodes: newNodes, links: links };
        
        // modify scope to trigger viz change
        $scope.nodes = obj;
        
        // increment offset
        $scope.offset = offsetAdj;
       
    };
    
    /*******************************/
    /********* !FUNCTIONS **********/
    /*******************************/
    
    // get data
	getDocs("similarity", "d");
    
	function getDocs(endpoint, id) {
		dataService.getData(endpoint, id).then(function(data) {
                        
            // assign to scope
			$scope.allNodes = data;
            
            // set current batch
            // separate from all in case we want to lazy load in the future
            $scope.nodes = data;
            
            // set button status based on call result
            $scope.isDisabled = $scope.allNodes.nodes.length > 0 ? false : true;
            
            // get features
            //getFeatures("classification", data.nodes[0].id);
           
		});
		
	};
    
    function getFeatures(endpoint, id) {
		dataService.getData(endpoint, id).then(function(data) {
            
            // assign to scope
            //$scope.features = data.features;
           
		});
		
	};
    	
}]);