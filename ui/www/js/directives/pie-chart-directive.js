angular.module("pie-chart-directive", [])

.directive("pieChart", ["d3Service", "dataService", "$stateParams", "$state", function(d3Service, dataService, $stateParams, $state) {
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
                var radius = Math.min(width, height) / 2;
				var color = ["orange", "teal", "grey", "#5ba819"];
				
				var arc = d3.svg.arc()
					.outerRadius(radius - 10)
					.innerRadius(radius - 70);

				var pie = d3.layout.pie()
					.sort(null)
					.padAngle(0.03)
					.value(function(d) { return d.population; });

                // create svg canvas
                var canvas = d3.select(element[0])
                    .append("svg")
                    .attr({
                        viewBox: "0 0 " + width + " " + height
                    })
					.append("g")
					.attr({
						transform: "translate(" + width / 2 + "," + height / 2 + ")"
					});
                
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

						var g = canvas.selectAll(".arc")
							  .data(pie(data))
							.enter().append("g")
							  .attr("class", "arc");

						  g.append("path")
							  .attr("d", arc)
							  .style("fill", function(d, i) { return color[i]; });

						  g.append("text")
							  .attr("transform", function(d) { return "translate(" + arc.centroid(d) + ")"; })
							  .attr("dy", ".35em")
							  .text(function(d) { return d.data.age; });
							
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