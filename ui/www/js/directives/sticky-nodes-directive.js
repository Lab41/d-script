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
                var radius = 4;
                var diameter = radius * 2;
				var color = ["orange", "teal", "grey", "#5ba819"];
				
				var force = d3.layout.force()
					.charge(-1000)
                    .linkDistance(270)
                    .size([(width - diameter), (height - diameter)]);
                
                var container = d3.select(element[0])
                    .append("div");
                
                // create html5 canvas
                var canvas = container
                    .append("canvas")
                    .attr({
                        height: height,
                        width: width
                    });
                
                var context = canvas.node().getContext("2d");
                
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
                            
                            // convert ids to index for d3
                            var idLinks = [];
                            
                            data.links.forEach(function(e) {
                                return {
                                    source: parseInt(e.source),
                                    target: parseInt(e.target),
                                    value: parseInt(e.value)
                                }
                            });
                            
                            var colorRange = ["white", "currentColor"];
                            
                            // min/max value
                            var minValue = d3.min(data.links, function(d) { return d.value; });
                            var maxValue = d3.max(data.links, function(d) { return d.value; });
                           
                            // create color scale
                            var colorScale = d3.scale.linear()
                                .domain([minValue, maxValue])
                                .range(colorRange);

                            // set layout data
							force
							  .nodes(data.nodes)
							  .links(data.links)
                                .on("tick", tick)
							  .start();

                            function tick() {
                            context.clearRect(0, 0, width, height);

                            // draw links
                            context.strokeStyle = "rgba(35,34,34,0.15)";
                                context.lineWidth = 0.1;
                            context.beginPath();
                            data.links.forEach(function(d) {
                              context.moveTo(d.source.x, d.source.y);
                              context.lineTo(d.target.x, d.target.y);
                            });
                            context.stroke();

                            // draw nodes
                            context.fillStyle = "currentColor";
                            context.beginPath();
                            data.nodes.forEach(function(d) {//console.log(d);
                              context.moveTo(d.x, d.y);
                              context.arc(d.x, d.y, radius, 0, 2 * Math.PI);
                            });
                            context.fill();
                          };
                            
                            // canvas click event
                            var el = document.getElementsByTagName("canvas")[0];
                            var offsetX = el.parentElement.parentElement.parentElement.parentElement.parentElement.offsetLeft;
                            var offsetY = 220;//var offsetY = parseInt(el.parentElement.parentElement.parentElement.parentElement.offsetTop) + parseInt(el.parentElement.parentElement.parentElement.offsetTop) + parseInt(el.parentElement.parentElement.offsetTop);

                            el.onclick = function(e) {console.log("canvas");
                                
                                var vizScope = scope.$parent;
                                
                                // get mouse coords
                                var mouseX = parseInt(e.clientX - offsetX);
                                var mouseY = parseInt(e.clientY - offsetY);
                                
                                // check that click is within bounds of a node
                                data.nodes.forEach(function(node) {
                                    
                                    var dx = mouseX - node.x;
                                    var dy = mouseY - node.y;
                                    
                                    if ((dx * dx) + (dy * dy) < radius * radius) {
                                        
                                        // draw circle hopefully over a node
                                        context.fillStyle = "#83f5f5";
                                        context.beginPath();
                                        context.arc(node.x, node.y, radius, 0, 2 * Math.PI);
                                        context.fill();
                                        
                                        // create new data object
                                        var newData = { id: node.id + "_1" };
                                        		
                                            dataService.getData("similarity/fragment", "001_1").then(function(data) {

            
                                        // assign to scope
                                        vizScope.details = [newData].concat(vizScope.details);
                                        console.log(vizScope.details);
                                            });
                                    };
                                    
                                });
                                
                            };
                            
                            // add svg for psuedo clicks and dummy doc
                            /*var svg = container
                                .append("svg")
                                .attr({
                                    id: "docs",
                                    viewBox: "0 0 " + width + " " + height
                                });
                            
                            var docNodes = scope.$parent.docNodes;
                            
                            var force2 = d3.layout.force()
                                .charge(-20)
                                .linkDistance(50)
                                .size([(width - diameter), (height - diameter)]);
                            
                            force2
                            .nodes(docNodes.nodes)
							  .links(docNodes.links)
                                .on("tick", dummy)
							  .start();
                            
                             var node = svg
                                .selectAll(".node")
                                .data(docNodes.nodes)
                                .enter()
                                .append("circle")
                                .attr({
                                    class: "node",
                                    r: radius
                                });
                            
                            function dummy() {
                                
                                node.attr("cx", function(d) { return d.x; })
					               .attr("cy", function(d) { return d.y; });  
                                
                            }*/
							
                        };
                        
                    };
                    
                });
				
			});
			
		}
		
	};
}]);