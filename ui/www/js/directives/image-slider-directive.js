angular.module("image-slider-directive", [])

.directive("imageSlider", [ function() {
	return {
		restrict: "E",
		scope: {
			vizData: "=",
            layout: "="
		},
        controller: function($scope) {
                        
             // control slider navigation
            $scope.currentIndex = 0;

            $scope.setCurrentSlideIndex = function(idx) {
                $scope.currentIndex = idx;
            };

            $scope.isCurrentSlideIndex = function(idx) {
                return $scope.currentIndex === idx;
            };

            $scope.previous = function() {
                $scope.currentIndex = ($scope.currentIndex < $scope.vizData.length - 1) ? ++$scope.currentIndex : 0;
            };

            $scope.next = function() {
                $scope.currentIndex = ($scope.currentIndex > 0) ? --$scope.currentIndex : $scope.vizData.length - 1;
            };
            
        },
		templateUrl: "templates/image-slider.html",
		link: function(scope, element, attrs) {
			
		}
		
	};
}]);