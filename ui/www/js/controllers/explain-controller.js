angular.module("explain-controller", [])

.controller("explainCtrl", ["$scope", "dataService", function($scope, dataService) {
    
    /**************************/
    /********* !DATA **********/
    /**************************/
    
    $scope.details = [];
    $scope.features;
    
	$scope.allNodes;
    $scope.nodes;
    $scope.docNodes;
    $scope.allDocNodes;
    $scope.offset = 0; // starting point   
    $scope.layout = "Grid";
    
    
    /****************************/
    /********* !EVENTS **********/
    /****************************/
    
    // add new node
    $scope.addNode = function(id) {
        
        // add dummy node
        // might be API call?
        var allNodes = $scope.nodes.nodes;
        var links = $scope.nodes.links;
        var newNodes = allNodes.concat({"id": "001"});
        var newLinks = links.concat({"source": 0, "target": 180, "value": "83.7159"});
        
        var obj = {nodes: newNodes, links: links};
        
        // add to scope to trigger viz change
        $scope.nodes = obj;
        
        // disable button
        $scope.isDisabled = true;
        
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
    
    $scope.toggleLayout = function() {
        $scope.layout = $scope.layout == "Grid" ? "Stack" : "Grid";// indicates which layout user is navigating to
    };
    
    
    
    /*******************************/
    /********* !FUNCTIONS **********/
    /*******************************/
    
    // get data
    getData("static", "author_adjacency");
    
	function getData(endpoint, id) {
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
    
    function getDummyData(endpoint, id) {
		dataService.getData(endpoint, id).then(function(data) {
                        
            // assign to scope
			$scope.allDocsNodes = data;
            
            // set current batch
            // separate from all in case we want to lazy load in the future
            $scope.docNodes = data;
           
		});
		
	};
    
    function getFeatures(endpoint, id) {
		dataService.getData(endpoint, id).then(function(data) {
            
            // assign to scope
            //$scope.features = data.features;
           
		});
		
	};
    	
}]);