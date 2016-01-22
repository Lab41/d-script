angular.module("sticky-nodes-directive", [])

.directive("stickyNodes", ["d3Service", "dataService", "$stateParams", "$state", function(d3Service, dataService, $stateParams, $state) {
	return {
		restrict: "E",
		scope: {
			vizData: "=",
            canvasWidth: "=",
            canvasHeight: "=",
			title: "="
		},
		template: "<p>{{ title }}</p>",
		link: function(scope, element, attrs) {
			
			// get d3 promise
			d3Service.d3().then(function(d3) {
                                
                // set sizes from attributes in html element
                // if not attributes present - use default
				var width = parseInt(attrs.canvasWidth) || 700;
                var height = parseInt(attrs.canvasHeight) || width;
                var radius = 10;
                var diameter = radius * 2;
				var color = ["orange", "teal", "grey", "#5ba819"];
				
				var force = d3.layout.force()
					.charge(-10)
                    .linkDistance(260)
                    .size([(width - diameter), (height - diameter)]);
                
                var svg = d3.select(element[0])
                    .append("svg")
                    .attr({
                        viewBox: "0 0 " + width + " " + height
                    });
                
                // bind data
                scope.$watch("vizData", function(newData, oldData) {
                    //console.log("--------------------- watch triggered ---------------------");
                    //console.log("------- old data -------"); console.log(oldData);
                    //console.log("------- new data -------"); console.log(newData);
    
                    // async check
                    if (newData !== undefined) {
                        //console.log("data is ready");
						
						// check new vs old
                        var isMatching = angular.equals(newData, oldData);
                        
                        // if false
                        if (!isMatching) {

                            // update the viz
                            draw(newData);

                        };
                        
                        function draw(data) {  
                            
                            force
							  .nodes(data.nodes)
							  .links(data.links)
                                .on("tick", tick)
							  .start();
                            
                             var node = svg
                                .selectAll(".node")
                                .data(data.nodes)
                                .enter()
                                .append("circle")
                                .attr({
                                    class: "node",
                                    r: radius
                                });
                            
                            // events
                            node
                                .on({
                                click: function(d) {
                                    
                                    // make node active
                                    // figure out how to make element work with SVG
                                    //angular.element(this).toggleClass = "active";
                                    
                                    var isActive = d3.select(this).attr("class") == "node active" ? true : false;
                                    
                                    // check class
                                    if (isActive) {
                                        
                                        // make inactive
                                        d3.select(this)
                                            .attr({
                                                class: "node"
                                            });
                                        
                                        // remove text marker
                                        d3.select("#t-" + d.id)
                                            .remove();
                                        
                                    } else {
                                        
                                        // make active
                                        d3.select(this)
                                            .attr({
                                                class: "node active"
                                            });
                                        
                                        // add text marker
                                        d3.select("svg")
                                            .append("text")
                                            .attr({
                                                id: "t-" + d.id,
                                                dx: this.cx.baseVal.value,
                                                dy: this.cy.baseVal.value
                                            })
                                            .text(d.id);
                                        
                                    };
                                    
                                    // get attribute data for individual node
                                    dataService.getData("similarity/fragment", "001_1").then(function(data) {
                                        
                                        var vizScope = scope.$parent;
                                        var newArray = [];
                                        
                                        // check for state of the node
                                        if (isActive) {
                                            
                                            // loop through detail object
                                            for (var i=0; i < vizScope.details.length; i++) {
                                                
                                                if (vizScope.details[i].id.split("_")[0] == d.id) {

                                                } else {
                                                    
                                                    // push value into new array
                                                    newArray.push(vizScope.details[i]);
                                                    
                                                }
                                                
                                            };
                                            
                                            // assign to scope
                                            vizScope.details = newArray;
                                            
                                        } else {
                                        
                                            // create new data object
                                            var newData = { id: d.id + "_1" };

                                            // assign to scope
                                            vizScope.details = [newData].concat(vizScope.details);
                                            
                                        };

                                    });
                                                                        
                                }
                            });
                            
                            function tick() {
                                
                                node.attr("cx", function(d) { return d.x; })
					               .attr("cy", function(d) { return d.y; });  
                                
                            };
                                
                        };
                        
                    };
                    
                });
				
			});
			
		}
		
	};
}]);