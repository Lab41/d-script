angular.module("module-title-directive", [])

.directive("moduleTitle", ["dataService", "$stateParams", "$state", function(dataService, $stateParams, $state) {
	return {
		restrict: "E",
		scope: {
            meta: "=",
            allModules: "="
        },
        templateUrl: "templates/directives/module-title.html",
        controller: function($scope, $element, $attrs) {
			
			// parent scopes
			var mainScope = $scope.$parent.$parent.$parent;
            var vizScope = $scope.$parent.$parent;
            
            // title
            $scope.isActive = false;

            // select title dropdown
            $scope.activeButton = function(e) {
                $scope.isActive = !$scope.isActive;
            };
            
            // change the tool data
            $scope.changeTool = function(idx, parentIdx) {
                
                // selected module
                var selectedModule = $scope.allModules[parentIdx];
                
                // detect if choosing a commit or a tool
                // change commit
                if ($attrs.meta == "commit") {
					
					// because commit is reset, get default items
					dataService.getItems(selectedModule.name, "flare").then(function(data) {

						// item attributes for URL
						var itemString = data.name;
                        
                        // set params for use
                        mainScope.urlParams = {
                            type: $state.params.type,
                            sections: mainScope.urlParams.sections,
                            tool: $state.params.tool,
                            commit: selectedModule.name,
                            items: itemString,
                            status: "all",
                            host: "all",
                            services: "all"
                        };
                                               
						// change url state
						$state.go($state.$current.name, mainScope.urlParams);
                        
                        // set commit scope
                        vizScope.commit = selectedModule;

					});
                   
                // change tool
                } else {
                    
                    // get params for state change
                    dataService.getAttrs("commits", selectedModule.name).then(function(data) {

                        // current commit
                        var commit = data[0];
                        
                        // set current commit
                        vizScope.commit = commit;
						
						// because tool is reset, get default items
						dataService.getItems(commit.name, "flare").then(function(data) {

							// item attributes for URL
							var itemString = data.name;
							
							// set params for use
							mainScope.urlParams = {
                                type: $state.params.type,
                                sections: mainScope.urlParams.sections,
								tool: selectedModule.name,
								commit: commit.name,
								items: itemString,
                                status: "all",
                                host: "all",
                                services: "all"
							};
							
							// change url state
							$state.go($state.$current.name, mainScope.urlParams);
							
							// set tool info
                        	mainScope.tool = selectedModule;
							
						});

                    });
                    
                };
                 
            };
        
        },
        link: function(scope, element, attrs) {

		}
		
	};
    
}]);