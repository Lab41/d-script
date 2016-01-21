angular.module("venn-diagram-directive", [])

.directive("vennDiagram", ["d3Service", "dataService", "$stateParams", "$state", function(d3Service, dataService, $stateParams, $state) {
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
				var color = ["orange", "teal", "grey", "#5ba819"];

                // create svg canvas
                var canvas = d3.select(element[0])
                    .append("svg")
                    .attr({
                        viewBox: "0 0 " + width + " " + height
                    });
				
				var defs = canvas.append("defs");
                
                // bind data
                scope.$watch("vizData", function(newData, oldData) {
                    //console.log("--------------------- watch triggered ---------------------");
                    //console.log("------- old data -------"); console.log(oldData);
                    //console.log("------- new data -------"); console.log(newData);
    
                    // async check
                    //if (newData !== undefined) {
                        //console.log("data is ready");
						
						// check new vs old
                        //var isMatching = angular.equals(newData, oldData);
                        
                        // if false
                        //if (!isMatching) {

                            // update the viz
                            draw(newData);

                        //};
                        
                        function draw(data) {
							
							defs
								.selectAll("clipPath")
								.data(data)
								.enter()
								.append("clipPath")
								.attr({
									id: function(d) { return "circle" + d.id; }
								})
								.append("circle")
								.attr({
									cx: function(d) { return d.cx; },
									cy: function(d) { return d.cy; },
									r: 180
								});
							
							// add background for ven element
							canvas
								.selectAll(".venn")
								.data(data)
								.enter()
								.append("rect")
								.attr({
								"clip-path": function(d) { return "url(#circle" + d.id + ")"; },
									width: width,
									height: height
								})
								.style({
									fill: function(d) { return color[d.id]; }
								});

canvas.append("g")
    .attr("clip-path", "url(#circle1)")
  .append("rect")
    .attr("clip-path", "url(#circle2)")
    .attr("width", width)
    .attr("height", height)
    .style("fill", "#4f6d6d");

canvas.append("g")
    .attr("clip-path", "url(#circle2)")
  .append("rect")
    .attr("clip-path", "url(#circle3)")
    .attr("width", width)
    .attr("height", height)
    .style("fill", "#617c55");

canvas.append("g")
    .attr("clip-path", "url(#circle3)")
  .append("rect")
    .attr("clip-path", "url(#circle1)")
    .attr("width", width)
    .attr("height", height)
    .style("fill", "#2e8e71");

canvas.append("g")
    .attr("clip-path", "url(#circle3)")
  .append("g")
    .attr("clip-path", "url(#circle2)")
  .append("rect")
    .attr("clip-path", "url(#circle1)")
    .attr("width", width)
    .attr("height", height)
    .style("fill", "#354848");
							
                        };
                        
                    //};
                    
                });
				
				function type(d) {
				  d.population = +d.population;
				  return d;
				}
				
			});
			
		}
		
	};
}]);