angular.module("explore-controller", [])

.controller("exploreCtrl", ["$scope", function($scope) {
    
    // viz tip slides
    $scope.slides = [
        {
            "name": "a01-030.png"
        },
        {
            "name": "a01-030u.png"
        },
        {
            "name": "a01-30x.png"
        }
    ];
    
    // control slider navigation
    $scope.currentIndex = 0;
    
    $scope.setCurrentSlideIndex = function(idx) {
        $scope.currentIndex = idx;
    };
    
    $scope.isCurrentSlideIndex = function(idx) {
        return $scope.currentIndex === idx;
    };
    
    $scope.previous = function() {
        $scope.currentIndex = ($scope.currentIndex < $scope.slides.length - 1) ? ++$scope.currentIndex : 0;
    };
    
    $scope.next = function() {
        $scope.currentIndex = ($scope.currentIndex > 0) ? --$scope.currentIndex : $scope.slides.length - 1;
    };
	
}]);