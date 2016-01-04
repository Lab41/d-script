angular.module("resize-buttons-directive", [])

.directive("resizeButtons", ["$state", "$stateParams", function($state, $stateParams) {
	return {
		restrict: "E",
        scope: {
            sectionName: "="
        },
        templateUrl: "templates/directives/resize-buttons.html",
        controller: function($scope, $state, $stateParams, $attrs) {
			
			// set button visibility
			$scope.setVisible = $state.$current.name == 'app.dashboard.set' ? true : false;
			$scope.detailVisible = $state.$current.name == 'app.dashboard.detail' ? true : false;
				
			// expand event
			$scope.expand = function() {
				
				var vizScope = $scope.$parent.$parent;
				var mainScope = vizScope.$parent;
			
				// hide set
				mainScope.setVis = false;

				// show detail
				mainScope.detailVis = true;
				
				// save params for toggling between states
				mainScope.urlParams = {
					type: $state.params.type,
					sections: $state.params.sections,
					tool: $state.params.tool,
					commit: $state.params.commit,
					items: $state.params.items,
					status: "all",
					host: "all",
					services: "all"
				};
				
				// change state
				$state.go("app.dashboard.detail", {
                    id: $attrs.sectionName,
					tool: $state.params.tool,
					commit: $state.params.commit
				});
				
			};
			
			// close event
			$scope.close = function() {
				
				var vizScope = $scope.$parent.$parent;
				var mainScope = vizScope.$parent;
			
				// hide detail
				mainScope.detailVis = false;

				// show set
				mainScope.setVis = true;
				
				// change state
				$state.go("app.dashboard.set", mainScope.urlParams, {
                    reload: true
                });
				
			};
                 
        },
        link: function(scope, element, attrs) {

		}
		
	};
    
}]);