angular.module("content-slider-directive", [])

.directive("contentSlider", ["$stateParams", function($stateParams) {
	return {
		restrict: "E",
		scope: {
			vizData: "="
		},
        controller: function($scope) {
            
            // look at sections
            angular.forEach($scope.vizData, function(value, key) {

                // return items based on state
                if (value.url == $stateParams.step) {

                    // set initial index for slider
                    $scope.currentIndex = key;

                };

            });

            $scope.setCurrentSlideIndex = function(idx) {
                $scope.currentIndex = idx;
            };

            $scope.isCurrentSlideIndex = function(idx) {
                return $scope.currentIndex === idx;
            };

            $scope.next = function() {
                
                // set current index
                $scope.currentIndex = ($scope.currentIndex < $scope.vizData.length - 1) ? ++$scope.currentIndex : 0;
                
                // set nav arrow values to match url routing
                setNav($scope.vizData);
                
            };

            $scope.previous = function() {
                
                // set current index
                $scope.currentIndex = ($scope.currentIndex > 0) ? --$scope.currentIndex : $scope.vizData.length - 1;
                
                // set nav arrow values to match url routing
                setNav($scope.vizData);
                
            };
            
            function setNav(sections) {
        
                // look at objects
                angular.forEach(sections, function(value, key) {

                    // return items based on state
                    if (value.url == $stateParams.step) {

                        var lastIdx = sections.length - 1;
                        var firstItem = sections[0];
                        var lastItem = sections[lastIdx];

                        // assign scope
                        $scope.nextStep = key == lastIdx ? firstItem.url : sections[key + 1].url;
                        $scope.previousStep = key == 0 ? lastItem.url : sections[key - 1].url;

                    };

                });

            };
            
        },
		templateUrl: "templates/directives/content-slider.html",
		link: function(scope, element, attrs) {
			
			scope.$watch("idx", function(newData, oldData) {
				
				// async check
				if (newData !== undefined) {
					//console.log("data is ready");

					// check new vs old
					var isMatching = angular.equals(newData, oldData);

					// if false
					if (!isMatching) {

						// control slider navigation
						scope.currentIndex = newData;

						scope.isCurrentSlideIndex = function(idx) {
							return scope.currentIndex === idx;
						};

					};
					
				};
				
			});
			
		}
		
	};
}]);