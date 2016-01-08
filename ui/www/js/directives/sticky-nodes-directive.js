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
                var radius = 2;
                var diameter = radius * 2;
				var color = ["orange", "teal", "grey", "#5ba819"];
				
				var force = d3.layout.force()
					.charge(-10)
                    .linkDistance(20)
					//.linkDistance(function(d) { return d.value; })
                    .size([(width - diameter), (height - diameter)])
					//.on("tick", tick);

				/*var drag = force.drag()
					.on("dragstart", dragstart);*/

                // create svg canvas
                var canvas = d3.select(element[0])
                    .append("svg")
                    .attr({
                        viewBox: "0 0 " + width + " " + height
                    });
				
				//var link = canvas.selectAll(".link");
    			//var node = canvas.selectAll(".node");
                
                // bind data
                scope.$watch("vizData", function(newData, oldData) {
                    console.log("--------------------- watch triggered ---------------------");
                    //console.log("------- old data -------"); console.log(oldData);
                    //console.log("------- new data -------"); console.log(newData);
    
                    // async check
                    if (newData !== undefined) {
                        //console.log("data is ready");
						
						// check new vs old
                        //var isMatching = angular.equals(newData, oldData);
                        
                        // if false
                        //if (!isMatching) {

                            // update the viz
                            draw(newData);

                        //};
                        
                        function draw(data) {

                            // set layout data
							force
							  .nodes(data.nodes)
							  .links(data.links)
							  .start();

						  /*link = link.data(data.links)
							.enter().append("line")
							  .attr("class", "link");
                            
                            node = node.data(force.nodes());
                          
                            
                            node.enter().append("circle").attr("class", function(d) { return "node " + d.id; }).attr("r", radius);
                          
                            // events
                            node.on({
                                click: function(d) {
                                    
                                    // show features
                                    d3.selectAll(".feature")
                                        .style({
                                            opacity: function(d) { return (d[0].value / 10); },
                                            fill: function(d, i) { return d[0].value > 9 ? "#e9f55c" : "currentColor"; }
                                        });
                                }
                            })
                            
                            node.exit().remove();*/
                            
                            var link = canvas
                                .selectAll(".link")
                                .data(data.links)
                                .enter()
                                .append("line")
                                .attr({
                                    class: "link"
                                })
                            
                            var node = canvas
                                .selectAll(".node")
                                .data(data.nodes)
                                .enter()
                                .append("circle")
                                .attr({
                                    class: "node",
                                    r: radius
                                })
                            
                            // events
                            node
                                .on({
                                click: function() {
                                    
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
                                        
                                    } else {
                                        
                                        // make active
                                        d3.select(this)
                                            .attr({
                                                class: "node active"
                                            });
                                        
                                    };
                                    
                                    // get attribute data for individual node
                                    dataService.getData("classification", "a").then(function(data) {
                                        
                                        var vizScope = scope.$parent;
                        
                                        // assign to scope
                                        vizScope.details = vizScope.details.concat(data);

                                    });
                                                                        
                                }
                            })
                                //.call(force.drag);
                            
                            force
                                .on("tick", function() {
                                
                                link.attr("x1", function(d) { return d.source.x; })
                                    .attr("y1", function(d) { return d.source.y; })
                                    .attr("x2", function(d) { return d.target.x; })
                                    .attr("y2", function(d) { return d.target.y; });
                                        
                                        node.attr("cx", function(d) { return d.x; })
                                            .attr("cy", function(d) { return d.y; });
                                        
                                    }
                                )
							
                        };
                        
                    };
                    
                });
				
				/*function tick() {
				  link.attr("x1", function(d) { return d.source.x; })
					  .attr("y1", function(d) { return d.source.y; })
					  .attr("x2", function(d) { return d.dest.x; })
					  .attr("y2", function(d) { return d.dest.y; });

				  node.attr("cx", function(d) { return d.x; })
					  .attr("cy", function(d) { return d.y; });
				}

				function dblclick(d) {
				  d3.select(this).classed("fixed", d.fixed = false);
				}

				function dragstart(d) {
				  d3.select(this).classed("fixed", d.fixed = true);
				}*/
				
			});
			
		}
		
	};
}]);