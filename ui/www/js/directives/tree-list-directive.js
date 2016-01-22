angular.module("tree-list-directive", [])

// tree
.directive("treeList", [function() {
	return {
		restrict: "E",
		template: "<ul><branch ng-repeat='c in vizData.children' viz-data='c'></branch></ul>",
		scope: {
			vizData: "="
		}
	};
    
}])

// branch
.directive("branch", function($compile) {
    return {
        restrict: "E",
        replace: true,
        scope: {
            branch: "=vizData"
        },
        template: "<li class='collapsed'><div><span id='{{ branch.name }}-tl'>{{ branch.name }}</span><span>&#x25CF;</span><input type='checkbox' id='{{ branch.name }}-tl-cbx' name='treelist' value='{{ branch.name }}'><label for='{{ branch.name }}-tl-cbx'></label><span>{{ branch.children.length }}</span></div></li>",
        link: function(scope, element, attrs) {
            
            // add class
            element.addClass("depth-" + scope.branch.depth);
            
            // check if there are any children, otherwise we'll have infinite execution
            var has_children = angular.isArray(scope.branch.children);

            // check for children
            if (has_children) {
                
                // add branch
                element.append("<tree-list viz-data='branch'></tree-list>");

                // recompile Angular because of manual appending
                $compile(element.contents())(scope); 
                
            } else {
                
                // add a class so we can style differently
                // items that are at the bottom of the branch
                element.addClass("item");
                
            };

            // bind events
            element.on("click", function(event) {
            
                event.stopPropagation();
				
				var elBranch = angular.element(document.getElementById(event.target.id.split("-")[0] + "-tl"));
				var elCheckBox = angular.element(document.getElementById(event.target.id.split("-")[0] + "-tl-cbx"));

                
                // check for children
                if (has_children) {
                    
                    // toggle css class to change state
                    element.toggleClass("collapsed");
					element.toggleClass("open");
					
					// check state
					if (element.hasClass("open")) {
						
						elBranch.addClass("active");
						
					} else {
						
						elBranch.removeClass("active");
						
					};
                    
                } else {

					elBranch.toggleClass("active");
					
				};
				
				// wrap element in angular(element) so we can toggle classes in other viz
				// need to make smarter like a service so directives don't have to know about
				// other existing directives
				var el = angular.element(document.getElementById(event.target.id.split("-")[0] + "-cp"));
                var elHeatmap = angular.element(document.getElementById(event.target.id.split("-")[0] + "-hg-y"));

				// check that item is not already active
				if (!el.hasClass("active") && elBranch.hasClass("active")) {

					// make active
					el.addClass("active");

				} else if (el.hasClass("active") && !elBranch.hasClass("active")) {

					// make inactive
					el.removeClass("active");

				};
				
				// check for highlight selection
				if (elCheckBox[0] != undefined) {
					
					// check value
					if (elCheckBox[0].checked) {
					
						// add highlight class
						el.addClass("highlight");
						elBranch.addClass("highlight");
                        
                        // check if heatmap row exists
                        if (elHeatmap != null) {
                            
                            // add highligh class
                            elHeatmap.addClass("highlight");
                            
                        };
						
					} else {
						
						// unhighlight
						el.removeClass("highlight");
						elBranch.removeClass("highlight");
                        
                        // check if heatmap row exists
                        if (elHeatmap != null) {
                            
                            // remove highlight
                            elHeatmap.removeClass("highlight");
                            
                        };
						
					};
					
				};

            });     
            
        }
        
    };
    
});