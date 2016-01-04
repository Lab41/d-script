angular.module("checkbox-buttons-directive", [])

.directive("checkboxButtons", [function() {
	return {
		restrict: "E",
		scope: {
            formData: "="
        },
        templateUrl: "templates/directives/checkbox-buttons.html",
        controller: function($scope, $element, $attrs) {
                 
        },
        link: function(scope, element, attrs) {

		}
		
	};
    
}])

.directive("checkboxActive", ["$stateParams", "$state", function($stateParams, $state) {
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
                            
                            // regex for multiple selections
                            var regSelectValue = new RegExp(value);
                        
                            // check button set against param key
                            // need more specific regex
                            if (newData.set.match(regSelectValue)) {
                                                                   
                                // regex for params
                                var regParams = new RegExp(newData.value);

                                // check button value against param value
                                if($stateParams[value].match(regParams)) {
                                    
                                    // selected status
                                    var isChecked = attrs.$$element[0].checked;
                                    
                                    // check if already selected
                                    if (isChecked) {
                                        
                                        // uncheck it
                                        element.removeAttr("checked");
                                        
                                    } else {

                                        // add checked attribute
                                        element.attr("checked", "checked");
                                       
                                        // add state param to user params
                                        userParams[value] = newData.value;
                                        
                                    };

                                };

                            } else {

                                // add state param to user params
                                userParams[value] = $stateParams[value];

                            };
                            
                        };
                        
                    });
                   
                    // bind events
                    element.on("click", function(event) {
                        
                        // set up needed values
                        var param = event.target.name;
                        var value = event.target.value;
                        var paramsArray = $stateParams[param].split(",");
                        var setArray;
                        
                        // need to compare params array against button array
                        // then set the new params accordingly
                        
                        // construct new state params
                        /*angular.forEach(paramsArray, function(value, key) {
                            
                            var isSelected = attrs.$$element[0].checked;
                            
                            // button would have just been selected 
                            if (isSelected && newParams.indexOf(value) == -1 && value == param) {console.log("item is checked");

                                // keep value for params
                                this.push(value);
                                
                            };
                            
                        }, newParams);
                        
                        // don't allow all to go unchecked
                        if (newParams.length == 0) {
                            
                            // revert to last checked state
                            angular.element(event.target).attr("checked", "checked");
                            
                            // use existing params
                            userParams[param] = paramsArray.toString();
                            
                        } else {

                            // add state param to user params
                            userParams[param] = newParams.toString();
                            
                        };*/

                        // state change based on selection
                        $state.go("app.dashboard.set", userParams);

                    });
                    
                };
                
            });
            
        }
    }
}])