angular.module("stacked-bar-chart-directive", [])

.directive("stackedBarChart", ["d3Service", "dataService", "$stateParams", "$state", function(d3Service, dataService, $stateParams, $state) {
	return {
		restrict: "E",
		scope: {
			vizData: "=",
            canvasWidth: "=",
            canvasHeight: "=",
            gutter: "=",
			title: "=",
            orientation: "="
		},
		template: "<p ng-if='\'title != ''\''>{{ title }}</p>",
		link: function(scope, element, attrs) {
			
			// get d3 promise
			d3Service.d3().then(function(d3) {
                                
                // set sizes from attributes in html element
                // if not attributes present - use default
				var width = parseInt(attrs.canvasWidth) || 700;
                var height = parseInt(attrs.canvasHeight) || 100;
                var gutter = parseInt(attrs.gutter) || 0.5;
                var padding = 5;
				var color = ["orange", "teal", "grey", "#5ba819"];
                var colorRange = ["white", "teal"];
                
                // calculate active content size
                var xAxisHeight = (0.3 * height);// % of total canvas height
                var activeHeight = height - xAxisHeight - (padding * 2);
                var activeWidth = width - (padding * 2);
                
                // set up stack layout
                var stack = d3.layout.stack();

                // create svg canvas
                var canvas = d3.select(element[0])
                    .append("svg")
                    .attr({
                        viewBox: "0 0 " + width + " " + height
                    })
                    .append("g")
                    .attr({
                        transform: "translate(" + padding + "," + padding + ")"
                    })
                
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
                            
                            // max value
                            var maxValue = d3.max(data, function(d) { return d.value; });
                            
                            // create color scale
                            var colorScale = d3.scale.linear()
                                .domain([0, maxValue])
                                .range(colorRange);
                            
                            // map data for horizontal stack
                            var data = data.map(function(d) {
                                return [{
                                    y: /*d.value*/1,
                                    x: d.name,
                                    value: d.value
                                }];
                            });
                            
                            // initialize layout
                            stack(data)
                            
                            // map data for horizontal stack to invert x,y values
                            // y0 becomes x0
                            var data = data.map(function(group) {
                                return group.map(function(d) {
                                    return {
                                        x: d.y,
                                        y: d.x,
                                        x0: d.y0,
                                        value: d.value
                                    };
                                });
                            });
                            
                            //set x scale
                            var xScale = d3.scale.linear()
                                    .domain([0, d3.max(data, function (group) { return d3.max(group, function (d) { return d.x + d.x0; }); })])
                                    .range([0, activeWidth]);
                                //.domain(data.map(function (d) { return d[0].y; }))
                                //.rangeRoundBands([0, activeWidth, gutter]);

                            //set x axis
                            var xAxis = d3.svg.axis()
                                    .scale(xScale)
                                    .orient("bottom");
                            
                            // add bars
                            var bar = canvas
                                .selectAll(".feature")
                                .data(data)
                                .enter()
                                .append("rect")
                                .attr({
                                    class: "feature",
                                    x: function(d) { return xScale(d[0].x0); },
                                    y: 0,
                                    height: activeHeight,
                                    width: function(d) { return xScale(d[0].x); }
                                })
                                .style({
                                    fill: function(d) { return colorScale(d[0].value); }
                                });
                            
                            // events
                            bar.on({
                                click: function(d) {
                                    console.log(this);
                                    // show attributes
                                    d3.select("body")
                                        .append("div")
                                        .attr({
                                            class: "tool-tip"
                                        })
                                        .style({
                                            left: 0,
                                            top: 0
                                        })
                                        .append("p")
                                        .text(d[0].y);
                                }
                            })
                            
                            // add label
                            /*canvas
                                .selectAll(".label")
                                .data(data)
                                .enter()
                                .append("text")
                                .attr({
                                    class: "label",
                                    x: function(d) { return ( (xScale(d[0].x) / 2) + xScale(d[0].x0) ); },
                                    y: activeHeight / 1.7
                                })
                                .text(function(d) { return d[0].y + " | " + d[0].x + "%"; });
                            */
                            //add x axis
                            /*canvas
                                .append("g")
                                .attr({
                                    class: "axis",
                                    transform: "translate(0," + (height - xAxisHeight) + ")"
                                })
                                .call(xAxis);*/
	
                        };
                        
                    };
                    
                });
				
			});
			
		}
		
	};
}]);