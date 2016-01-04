angular.module("packed-circles-directive", [])

.directive("packedCircles", ["d3Service", "dataService", "$stateParams", "$state", function(d3Service, dataService, $stateParams, $state) {
	return {
		restrict: "E",
		scope: {
			vizData: "=",
            canvasWidth: "=",
            canvasHeight: "=",
            padding: "=",
            colorRange: "="
		},
		link: function(scope, element, attrs) {
			
			// get d3 promise
			d3Service.d3().then(function(d3) {
                                
                // set sizes from attributes in html element
                // if not attributes present - use default
				var width = parseInt(attrs.canvasWidth) || 700;
                var height = parseInt(attrs.canvasHeight) || width;
                var padding = parseInt(attrs.padding) || 15;
                var radius = (Math.min(width, height) - (padding * 2)) / 2;
                var diameter = radius * 2;
                
                // extra work to get a color array from an attribute
                // replace value commas with a pipe character so when we split later rgb values don't get broken
                // and replace quotes with nothing so our values can be consumed by d3
                var colorRange = attrs.colorRange ? attrs.colorRange.substring(1, attrs.colorRange.length - 1).replace(/',(\s+)?'/g,"|").replace(/'/g, "").split("|") : undefined || ["black", "grey", "darkgrey"];
                
                // set color
                var color = d3.scale
                    .linear()
                    .domain([-1, 5])
                    .range(colorRange)

                // create svg canvas
                var canvas = d3.select(element[0])
                    .append("svg")
                    .attr({
                        viewBox: "0 0 " + width + " " + height
                    })
                
                    // add group for slices
                    .append("g")
                    .attr({
						id: "packed-circles"/*,
                        transform: "translate(" + radius + "," + radius + ")"*/
                      });
                
                // set layout
                var pack = d3.layout
                    .pack()
                    .padding(3)
                    .size([diameter, diameter])
                    .value(function(d) { return d.size; });
                
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
                            
                            // set the title
                            scope.title = newData.name;

                            // update the viz
                            draw(newData);

                        };
                        
                        function draw(data) {
                            
                            // set hover text value
                            scope.$parent.$parent.hoverItem = { name: data.name };
                                             
                            pack.value(function(d) { return d.size; });

                            // set variables to use for zooming and data starting point (a.k.a. root)
                            var focus = data;
                            var nodes = pack.nodes(data);
                            var view;

                            // set selection
                            var circle = d3.select("#packed-circles")
                                .selectAll("circle")
                                .data(nodes);
                                             
                             // update selection
                            circle
                                .transition()
                                .duration(5000)
                                .attr({
                                    id: function(d) { return d.name + "-cp"; },
                                    class: function(d) { return d.parent ? d.children ? "node parent" : "node leaf" : "node root"; },
                                    //cx: function(d) { return d.x; },
                                    //cy: function(d) { return d.y; },
                                    transform: function(d) { return "translate(" + d.x + "," + d.y + ")"; },
                                    r: function(d) { return d.r; }
                                })
                                .style({
                                    //fill: function(d) { return d.children ? color(d.depth) : null; }
                                });

                            // enter selection
                            circle
                                .enter()
                                .append("circle")
                                .transition()
                                .duration(5000)
                                .attr({
                                    id: function(d) { return d.name + "-cp"; },
                                    class: function(d) { return d.parent ? d.children ? "node parent" : "node leaf" : "node root"; },
                                    //cx: function(d) { return d.x; },
                                    //cy: function(d) { return d.y; },
                                    transform: function(d) { return "translate(" + d.x + "," + d.y + ")"; },
                                    r: function(d) { return d.r; }
                                })
                                .style({
                                    //fill: function(d) { return d.children ? color(d.depth) : null; }
                                })

                            // set events
                            circle
                                .on({
                                    click: function(d) {
                                        
                                        // look for heatmap item
                                        var currentID = this.id.split("-")[0];
                                        var heatItem = document.getElementById(currentID + "-hg");
                                        
                                        // check that item is already in the heatmap grid
                                        if (heatItem == null) {
											
											var vizScope = scope.$parent.$parent;
                                        
                                            // populate selected item
                                            dataService.getItems(d.name).then(function(data) {
												
												// check for data !!!!
												if (data != "") {

													// add to selected items
													vizScope.items = vizScope.items.concat(data[0]);

													// get new data
													dataService.getItems($stateParams.commit, "grid", vizScope.timeStart, vizScope.timeEnd, d.name).then(function(data) {
														
														// check for data !!!!
														if (data != "") {
															
															// add new data line to heat map grid
															vizScope.dataGrid = vizScope.dataGrid.concat(data[0]);
															
														} else {
                                                            
                                                            // heat map no data
                                                            vizScope.dataGrid = vizScope.dataGrid.concat({dates: [], name: d.name });
                                                            
                                                        };

													});
													
												} else {
													
													// do something to indicate there was no data from the api call
													
                                                    // detail no data
													vizScope.items = vizScope.items.concat({ name: d.name });
                                                    
                                                    // heat map no data
                                                    vizScope.dataGrid = vizScope.dataGrid.concat({dates: [], name: d.name });
													
												};

                                            });
											
											var itemString = $state.params.items + "," + d.name;
                                            
                                        } else {
											
											var itemString = $state.params.items;
											
                                            // do some style thing here to call out row in heat grid
                                        
                                        };
                                        
                                        // clicked element
                                        var clickedElement = angular.element(this);

                                        // toggle css class to change state
                                        clickedElement.toggleClass("active");

                                        // wrap element in angular(element) so we can toggle classes in other viz
                                        // need to make smarter like a service so directives don't have to know about
                                        // other existing directives

                                        // check for root
                                        if (!angular.element(this).hasClass("root")) {

                                            // tree-list item
                                            var el = angular.element(document.getElementById(this.id.split("-")[0] + "-tl"));
											var elParent = angular.element(document.getElementById(this.id.split("-")[0] + "-tl").parentNode.parentNode); // if tree-list structure changes this must change
											var elCheckBox = angular.element(document.getElementById(this.id.split("-")[0] + "-tl-cbx"));
											
                                            // check that item is not already active
                                            if (!el.hasClass("active") && clickedElement.hasClass("active")) {
                                                
												// make active item
												el.addClass("active");

												// check highlight box
												//elCheckBox.attr("checked", true);
                                                
                                            } else if (el.hasClass("active") && !clickedElement.hasClass("active")) {
												
												// make item inactive
												el.removeClass("active");

												// remove highlight
												//elCheckBox.attr("checked", false);
												
											};
                                            
                                            // check if collapsed
                                            if (elParent.hasClass("collapsed") && clickedElement.hasClass("active")) {
                                                
                                                // uncollapse
                                                elParent.removeClass("collapsed");
												elParent.addClass("open");
                                                
                                            };
                                            
                                            // uncollapse up the tree
                                            stepThrough(d);

                                            function stepThrough(node) {

                                                // parent node
                                                var parent = node.parent;
                                                
                                                // check that parent is not the root
                                                if (parent.depth > 0) {
                                                    
                                                    // uncollapse
                                                    //console.log(parent.name + " " + parent.depth);
                                                    pNode = document.getElementById(parent.name + "-tl").parentNode.parentNode; // if the tree-list structure changes this must change
                                                    pEl = angular.element(pNode);

                                                    // check that item is not already active
                                                    if (!pEl.hasClass("open")) {

                                                        // make active
                                                        pEl.addClass("open");

                                                    };

                                                    // check if collapsed
                                                    if (pEl.hasClass("collapsed")) {

                                                        // uncollapse
                                                        pEl.removeClass("collapsed");

                                                    };
                                                    
                                                    // need to scroll to active area if not 
                                                    // already viewable


                                                    // check depth
                                                    if (parent.depth > 1) {

                                                        // recurse nodes
                                                        stepThrough(parent);

                                                    };
                                                    
                                                    
                                                };

                                                return;

                                            };

                                        };
                                        
                                        // check that element exists
                                        if (heatItem != null) {
                                        
                                            // set heatgrid item element
                                            var el = document.getElementById(currentID + "-hg-y");
                                            var elCircle = angular.element(this);

                                            // check circle state
                                            if (!el.classList.contains("active") && elCircle.hasClass("active")) {
                                                
                                                //add class
                                                d3.select(el)
                                                    .attr({
                                                        class: "item active"
                                                    });
                                                
                                            } else if (el.classList.contains("active") && !elCircle.hasClass("active")) {

                                                // remove class
                                                d3.select(el)
                                                    .attr({
                                                        class: "item"
                                                    });

                                            };
                                            
                                        };
										
										// change state
										$state.go("app.dashboard.set", {
											type: $state.params.type,
											sections: $state.params.sections,
											tool: $state.params.tool,
											commit: $state.params.commit,
											items: itemString,
											status: "all",
											host: "all",
											services: "all"
										}, {
											notify: false,
											reload: false
										});

                                    },
                                    mouseover: function(d) {
                                        
                                        var vizScope = scope.$parent.$parent;
                                        
                                        // change item 
                                        vizScope.hoverItem = {name: d.name};
                                        
                                    }
                                });

                            // exit selection
                            circle
                                .exit()
                                .transition()
                                .duration(5000)
                                .attr({
                                    transform: function(d) { return "translate(" + (width * 2) + "," + (height * 2) + ")"; }
                                })
                                .remove();

                            // set selection
                            var text = d3.select("#packed-circles")
                                .selectAll("text")
                                .data(nodes);

                            // enter selection
                            text
                                .enter()
                                .append("text")
                                .style({
                                    "fill-opacity": 0
                                });

                            // update selection
                            text
                                .transition()
                                .duration(5500)
                                .attr({
                                    x: function(d) { return d.x; },
                                    y: function(d) { return d.y; }
                                })
                                .style({
                                    "fill-opacity": function(d) { return d.parent === data ? 1 : 0; },
                                    display: function(d) { return d.parent === data ? "inline" : "none"; },
                                })
                                .text(function(d) { return d.name; });

                            // exit selection
                            text
                                .exit()
                                .remove();

                        };
                        
                    };
                    
                });
				
			});
			
		}
		
	};
}]);