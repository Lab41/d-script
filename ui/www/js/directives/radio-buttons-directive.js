angular.module("radio-buttons-directive", [])

.directive("radioButtons", [function() {
	return {
		restrict: "E",
		scope: {
            formData: "="
        },
        templateUrl: "templates/directives/radio-buttons.html",
        controller: function($scope, $element, $attrs) {
                 
        },
        link: function(scope, element, attrs) {

		}
		
	};
    
}])

.directive("radioActive", ["$stateParams", "$state", function($stateParams, $state) {
    return {
        restrict: "A",
        link: function(scope, element, attrs) {
            
            // url params
            var params = Object.keys($stateParams);
            var urlString = $state.current.url;
            
            // watch radio check
            scope.$watch("optionItem", function(newData, oldData) {
                
                // compile check
                if (newData !== undefined) {
                    
                    // set up object to capture url params
                    var userParams = {};
                    
                    // check params
                    angular.forEach(params, function(value, key) {
                        
                        // regex of param value
                        var regValue = new RegExp(value);
                        
                        // check that param is in current state
                        // and not actually in a parent state
                        var inCurrent = urlString.match(regValue);
                        
                        if (inCurrent) {
                        
                            // check button set against param key
                            if (newData.set == value) {

                                // check button value against param value
                                if(newData.value == $stateParams[value]) {

                                    // add checked attribute
                                    element.attr("checked", "checked");

                                };

                                // add state param to user params
                                userParams[value] = newData.value;

                            } else {

                                // add state param to user params
                                userParams[value] = $stateParams[value];

                            };
                            
                        };
                        
                    });
                    
                    // bind events
                    element.on("click", function(event) {

                        // state change based on selection
                        $state.go("app.dashboard.set", userParams);

                    });
                    
                };
                
            });
            
        }
    }
}])