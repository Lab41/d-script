angular.module("spark-line-directive", [])

.directive("sparkLine", ["d3Service", "moment", function(d3Service, moment){
    return {
        restrict: "E",
        scope: {
            vizData: "=",
            canvasWidth: "=",
            canvasHeight: "="
        },
        link: function(scope, element, attrs){
            
            //get d3 promise
            d3Service.d3().then(function(d3) {
                
                // set sizes from attributes in html element
                // if not attributes present - use default
                var width = parseInt(attrs.canvasWidth) || 400;
                var height = parseInt(attrs.canvasHeight) || 200;
                
                // format the date
                var parseDate = d3.time.format("%Y-%m-%d").parse;
                
                // need some padding so the viewBox doesn't cut off the ends of the line
                var linePadding = 10;
                var axisHeight = linePadding * 1.5;
                var commitLength = 6; // need to make smarter so it's the width of the axis slice
                
                // x-scale
                var xScale = d3.time.scale()
                    .range([linePadding, (width - linePadding)]);
                
                // y-scale
                var yScale = d3.scale.linear()
                    .range([axisHeight, (height -linePadding)]);
                
                // x-axis
                var xAxis = d3.svg.axis()
                    .scale(xScale)
                    .ticks(d3.time.day, 1)
                    .tickFormat(d3.time.format("%d"))
                    .orient("top");
                
                // y-axis
                var yAxis = d3.svg.axis()
                    .scale(yScale)
                    .orient("left");
                
                // spark line
                var sparkline = d3.svg.line()
                    .x(function(d) { return xScale(d.date); })
                    .y(function(d) { return yScale(d.count); })
                    .defined(function(d) { return d.count > 0; });
                                
                // create svg canvas
                var canvas = d3.select(element[0])
                    .append("svg")
                    .attr({
                        viewBox: "0 0 " + width + " " + height
                    });
                
                // background
                canvas
                    .append("rect")
                    .attr({
                        x: 0,
                        y: axisHeight,
                        width: width,
                        height: (height - axisHeight)
                    })
				
                // check for new data
                scope.$watch("vizData", function(newData, oldData) {
                    //console.log("--------------------- watch triggered ---------------------");
                    //console.log("------- old data -------"); console.log(oldData);
                    //console.log("------- new data -------"); console.log(newData);
                    // async check
                    if (newData !== undefined) {
						//console.log("data is ready")
                        // check new vs old
                        var isMatching = angular.equals(newData, oldData);

                        // if false
                        if (!isMatching) {

                            // update the viz
                            draw(newData);

                        };
                        
                        function draw(data) {
                            
                            data.forEach(function(d) {
                                d.date = parseDate(d.date);
                                d.count = d.commits.length;
                            });
                            //console.log(data);
                            xScale.domain(d3.extent(data, function(d) { return d.date; }));
                            yScale.domain(d3.extent(data, function(d) { return d.count; }));
                            
                            // set selection
                            var line = canvas
                                .selectAll("path")
                                .data([data]);
                            
                            // update selection
                            line
                                .transition()
                                .duration(5000)
                                .ease("linear")
                                .attr({
                                    d: sparkline
                                });
                            
                            // enter selection
                            line
                                .enter()
                                .append("path")
                                .transition()
                                .duration(5000)
                                .attr({
                                    d: sparkline
                                });
                            
                            // exit selection
                            line
                                .exit()
                                .transition()
                                .duration(5000)
                                .attr({
                                    d: sparkline
                                })
                                .remove();
                            
                            // add points for each commit (time of day)
                            canvas
                                .selectAll(".commit-day")
                                .data(data.filter(function(d) { return d.count; }))
                                .enter()
                                .append("g")
                            
                                .each(function(d) {
                                
                                    d3.select(this)
                                        .append("circle")
                                        .attr({
                                            cx: xScale(d.date),
                                            cy: yScale(d.count),
                                            r: 1
                                        });
                                    
                                    var dayGroup = d3.select(this);                                
                                    var commitHeight = 6; // need to make smarter based on scale
                                
                                    // each commit
                                    dayGroup
                                        .selectAll(".commit")
                                        .data(d.commits)
                                        .enter()
                                        .append("line")
                                        .attr({
                                            class: "commit",
                                            x1: xScale(d.date) - commitLength,
                                            y1: function(a, i) { return yScale(d.count) + (i * commitHeight); },
                                            x2: xScale(d.date) + commitLength,
                                            y2: function(a, i) { return yScale(d.count) + (i * commitHeight); }
                                        });
                                
                                    // each label for commit
                                    dayGroup
                                        .selectAll(".commit-text")
                                        .data(d.commits)
                                        .enter()
                                        .append("text")
                                        .attr({
                                            class: "commit-text",
                                            x: xScale(d.date) + (commitLength * 2),
                                            y: function(a, i) { return yScale(d.count) + (i * commitHeight + 2); }
                                        })
                                        .text(function(a) { return a.name; });
                                
                                });
                            
                            // add x-axis
                            canvas
                                .append("g")
                                .attr({
                                    class: "x-axis",
                                    transform: "translate(0," + (linePadding * 2) + ")"
                                })
                                .call(xAxis);

                        };
                        
                    };
                    
                });       
                
            });
            
        }
    }
    
}]);