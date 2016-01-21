angular.module("heatmap-grid-directive", [])

.directive("heatmapGrid", ["d3Service", "dataService", "moment", "$state", function(d3Service, dataService, moment, $state){
    return {
        restrict: "E",
        scope: {
            vizData: "=",
            canvasWidth: "=",
            canvasHeight: "=",
            steps: "=",
            gutter: "=",
            padding: "=",
            yAxisWidth: "=",
            xAxisHeight: "=",
            colorRange: "="
        },
        controller: function($scope) {
            
            var vizScope = $scope.$parent.$parent;
            
            $scope.prevText;
            $scope.nextText;
            $scope.endDate;
            $scope.startDate;
            
            // transition date ranges in heatmap grid
            // accepts "previous" or "next" as valid
            // text for the direction param
            $scope.newDates = function(direction) {

                // current values
                var oldStart = $scope.startDate;
                var oldEnd = $scope.endDate;
                var oldDuration = vizScope.timeDuration;
                var datesStart = vizScope.datesStart; // earliest available date
                var datesEnd = vizScope.datesEnd; // latest available date

                // using existing duration these are the
                // max start and end dates possible
                var tempStartPrev = moment(oldStart).subtract(oldDuration, "days").format("YYYY-MM-DD");
                var tempEndNext = moment(oldEnd).add(oldDuration, "days").format("YYYY-MM-DD");

                // check for range usability
                if (moment(tempStartPrev).isSame(datesStart, "day")) {

                    var isPast = true;

                } else if (moment(tempStartPrev).isBefore(datesStart, "day")) {

                    var isPast = true;

                };

                // check direction
                if (direction == "previous") {

                    // check that dates are within range of available data
                    if (!isPast) {

                        // calculate dates
                        var end = moment(oldStart).subtract(1, "days").format("YYYY-MM-DD");
                        var start = moment(end).subtract(oldDuration, "days").format("YYYY-MM-DD");

                    } else {

                        // calculate how many dates from the old start are available in data
                        // subtract 5 to remove inclusive dates in the difference
                        // and the range for the viz doesn't repeat start/end range dates
                        var eligibleDates = moment(oldStart).diff(tempStartPrev, "days") - 5;

                        // calculate dates
                        var end = moment(oldStart).subtract(1, "days").format("YYYY-MM-DD");
                        var start = moment(end).subtract(eligibleDates, "days").format("YYYY-MM-DD");

                    };

                    // enable next button
                    var isFuture = false;

                } else {

                    // check that dates are within range of available data
                    if (!isFuture) {

                        // calculate dates
                        var start = moment(oldEnd).add(1, "days").format("YYYY-MM-DD");
                        var end = moment(start).add(oldDuration, "days").format("YYYY-MM-DD");

                    } else {

                        // calculate how many dates from the old start are available in data
                        // subtract 5 to remove inclusive dates in the difference
                        // and the range for the viz doesn't repeat start/end range dates
                        var eligibleDates = moment(oldEnd).diff(moment(), "days");
                        
                        // calculate dates
                        var start = moment(oldEnd).add(1, "days").format("YYYY-MM-DD");
                        var end = moment(start).add(eligibleDates, "days").format("YYYY-MM-DD");

                    };

                    // enable previous button
                    var isPast = false;

                };

                // check for range usability
                if (moment(end).isSame(datesEnd, "day")) {

                    var isFuture = true;

                } else if (moment(end).isAfter(datesEnd, "day")) {

                    var isFuture = true;

                };

                var structure = "grid";

                // get data for specified date range
                dataService.getItems("commit1", structure, start, end, "flare").then(function(data) {
            
                    // selected individual
                    vizScope.dataGrid = data;
                    
                    // set new dates to scope
                    $scope.startDate = start;
                    $scope.endDate = end;
                    $scope.isFuture = isFuture;
                    $scope.isPast = isPast;

                });

            };
            
        },
        templateUrl: "templates/directives/heatmap.html",
        link: function(scope, element, attrs){
            
            //get d3 promise
            d3Service.d3().then(function(d3) {
                
                // set sizes from attributes in html element
                // if not attributes present - use default
                var width = parseInt(attrs.canvasWidth) || 400;
                var height = parseInt(attrs.canvasHeight) || 200;
                var steps = parseInt(attrs.steps) || 5;
				var gutter = parseInt(attrs.gutter) || 10;
				var padding = parseInt(attrs.padding) || 20;
                var yLabelColumn = (parseInt(attrs.yAxisWidth) || 20) / 100;
                var xLabelRow = (parseInt(attrs.xAxisHeight) || 10) / 100;
                var xLabelRowLine = 10;
                
                // extra work to get a color array from an attribute
                // replace value commas with a pipe character so when we split later rgb values don't get broken
                // and replace quotes with nothing so our values can be consumed by d3
                var colorRange = attrs.colorRange ? attrs.colorRange.substring(1, attrs.colorRange.length - 1).replace(/',(\s+)?'/g,"|").replace(/'/g, "").split("|") : undefined || ["black", "darkgrey", "grey", "white"];
                
                // convert values to usable space calculations
                var activeXspace = width - (width * yLabelColumn);
                var activeYspace = height - (height * xLabelRow) - xLabelRowLine;
                                
                // create svg canvas
                var canvas = d3.select(element[0])
                    .append("svg")
                    .attr({
                        viewBox: "0 0 " + width + " " + height
                    });
                
                // add group for grid
                var gridWrap = canvas
                    .append("g")
					.attr({
						id: "heat-grid",
						transform: "translate(" + (padding + (yLabelColumn * width)) + ", " + (padding + (xLabelRow * height) + xLabelRowLine) + ")"
					});
                
                // add group for y labels
                var yLabelWrap = canvas
                    .append("g")
                    .attr({
						id: "heat-y-header",
                        transform: "translate(" + padding + "," + (padding + (xLabelRow * height) + xLabelRowLine) + ")"
                    });
                
                // add group for x labels
                var xLabelWrap = canvas
                    .append("g")
                    .attr({
						id: "heat-x-header",
                        transform: "translate(" + (padding + (yLabelColumn * width)) + "," + padding + ")"
                    });
				
                // check for new data
                scope.$watch("vizData", function(newData, oldData) {
                    //console.log("--------------------- watch triggered ---------------------");
                    //console.log("------- old data -------"); console.log(oldData);
                    //console.log("------- new data -------"); console.log(newData);
                    // async check
                    if (newData !== undefined) {
                    
                        // check new vs old
                        var isMatching = angular.equals(newData, oldData);

                        // if false
                        if (!isMatching) {

                            // update the viz
                            draw(newData);

                        };
                        
                        function draw(data) {
                            
                            var vizScope = scope.$parent.$parent;
                            
                            var start = data[0].dates[0].date;
                            var end = data[0].dates[data[0].dates.length - 1].date;
                            var timeSpan = data[0].dates.length;
                            
                            // set button visibility
                            var tempStartPrev = moment(start).subtract(timeSpan, "days").format("YYYY-MM-DD");
                            var tempEndNext = moment(end).add(timeSpan, "days").format("YYYY-MM-DD");
                            var isFuture = moment(tempEndNext).isAfter(moment(), "day") ? true : false;
                            var isPast = moment(tempStartPrev).isBefore(vizScope.datesStart, "day") ? true : false;
                            
                            // set button scope
                            scope.prevText = moment(start).calendar();
                            scope.nextText = moment(end).calendar();
                            scope.startDate = start;
                            scope.endDate = end;
                            //scope.isFuture = isFuture;
                            //scope.isPast = isPast;
                            
                            // rows/columns
                            var columnCount = timeSpan;
                            var rowCount = data.length;

                            // active space minus gutters and padding
                            var contentWidth = (activeXspace - (padding * 2) - (gutter * (columnCount - 1)));
                            var contentHeight = (activeYspace - (padding * 2) - (gutter * (rowCount - 1)));

                            // dimension of a single grid item
                            var tileWidth = contentWidth / columnCount; 
                            var tileHeight = contentHeight / rowCount;

                            // create color scale
                            var color = d3.scale.quantile()
                                .domain([0, steps - 1, /*d3.max(newData.values, function (d) { return d.value; })*/ 100])
                                .range(colorRange);
                                             
                            /********************/
                            /***** !BUTTONS *****/
                            /********************/
					
                            /****************/
                            /***** GRID *****/
                            /****************/

                            // set selection
                            var grid = d3.select("#heat-grid")
                                .selectAll(".row")
                                .data(data);

                            // enter selection
                            grid
                                .enter()
                                .append("g")
                                .attr({
                                    id: function(d) { return d.name + "-hg"; }
                                });

                            // update selection
                            grid
                                .each(function(row, i) {

                                // set row
                                var rowIdx = i;

                                // set selection
                                var columnGroup = d3.select(this)
                                    .selectAll(".tile")
                                    .data(row.dates);

                                // enter selection
                                columnGroup
                                    .enter()
                                    .append("g");

                                // update selection 
                                columnGroup
                                    .each(function(date, i) {

                                        // set date
                                        var dayIdx = i;

                                        // set wrap that holds tile and label
                                        var dayGroup = d3.select(this);

                                        // set selection
                                        var shape = dayGroup
                                            .selectAll("rect")
                                            .data([date]);

                                        // enter selection
                                        shape
                                            .enter()
                                            .append("rect")
                                            .style({
                                                fill: "rgb(44, 50, 50)"
                                            });

                                        // update selection
                                        shape
                                            .transition()
                                            .duration(1000)
                                            .attr({
                                                x: dayIdx * (tileWidth + gutter),
                                                y: rowIdx  * (tileHeight + gutter),
                                                width: tileWidth,
                                                height: tileHeight
                                            })
                                            .style({
                                                fill: function(d) { return color(d.value); }
                                            });

                                        // set selection
                                        var label = dayGroup
                                            .selectAll("text")
                                            .data([date]);

                                        // enter selection
                                        label
                                            .enter()
                                            .append("text");

                                        // update selection
                                        label
                                            /*.style({
                                                opacity: 0
                                            })*/
                                            .transition()
                                            .duration(1000)
                                            .delay(500)
                                            .attr({
                                                class: "label",
                                                x: (dayIdx * (tileWidth + gutter)) + (tileWidth / 2),
                                                y: (rowIdx  * (tileHeight + gutter)) + (tileHeight / 2)
                                            })
                                            /*.style({
                                                opacity: 1
                                            })*/
                                            .text(function(d) { return d.value; });

                                    })
                                    .attr({
                                        class: "tile"
                                    });

                                // exit selection
                                columnGroup
                                    .exit()
                                    .remove();

                                })
                                .attr({
                                    class: "row"
                                });

                            // exit selection
                            grid
                                .exit()
                                .remove();

                            /******************/
                            /***** Y-AXIS *****/
                            /******************/

                            // set selection
                            var column = d3.select("#heat-y-header")
                                .selectAll(".y-title")
                                .data(data);

                            // enter selection
                            column
                                .enter()
                                .append("g");
                            
                            // bind events
                            column
                                .on({
                                    click: function(d) {
                                        
                                        var vizScope = scope.$parent.$parent;
                                        
                                        // create new array to hold active items
                                        var array = [];
										
										// create sting to update URL
										var itemString = "";
                                        
                                        // loop through so we can return a new array for
                                        // the directive to $watch and act on
                                        angular.forEach(vizScope.dataGrid, function(value, key) {
                                            
                                            // check name
                                            if (value.name != d.name) {
                                                
                                                // push to new array
                                                this.push(value);
												
												// check for existing items
												if (itemString == "") {
													
													// add without comma
													itemString += value.name;
													
												} else {
													
													// add with comma
													itemString += "," + value.name;
													
												};												
												
                                            };
                                            
                                        }, array);
                                        
                                        // remove item from scope
                                        vizScope.dataGrid = array;
										
										// create new array to hold active items
                                        var array = [];
                                        
                                        // loop through so we can return a new array for
                                        // the directive to $watch and act on
                                        angular.forEach(vizScope.items, function(value, key) {
                                            
                                            // check name
                                            if (value.name != d.name) {
                                                
                                                // push to new array
                                                this.push(value);											
												
                                            };
                                            
                                        }, array);
                                        
                                        // remove item from scope
                                        vizScope.items = array;
										
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
                                        
                                    }
                                
                                });

                            // update selection
                            column
                                .each(function(row, i) {
                                
                                    // set row
                                    var rowIdx = i;

                                    // set wrap that holds tile and close icon
                                    var itemGroup = d3.select(this);
                                
                                    /****************/
                                    /***** TEXT *****/
                                    /****************/
                                
                                    // set selection
                                    var label = itemGroup
                                        .selectAll("text")
                                        .data([row]);

                                    // enter selection
                                    label
                                        .enter()
                                        .append("text");

                                    // update selection
                                    label
                                        .style({
                                            opacity: 0
                                        })
                                        .transition()
                                        .duration(1000)
                                        .attr({
                                            class: "y-axis",
                                            x: 10,
                                            y: function(d, i) { return (rowIdx  * (tileHeight + gutter)) + (tileHeight / 2) }
                                        })
                                        .style({
                                            opacity: 1
                                        })
                                        .text(function(d) { return d.name; });
                                
                                    /*****************/
                                    /***** CLOSE *****/
                                    /*****************/
                                
                                    // set selection
                                    var shape = itemGroup
                                        .selectAll(".icon")
                                        .data([row]);

                                    // enter selection
                                    shape
                                        .enter()
                                        .append("text");

                                    // update selection
                                    shape
                                        .transition()
                                        .duration(1000)
                                        .attr({
                                            class: "icon",
                                            x: 0, /* compute text length */
                                            y: function(d, i) { return (rowIdx  * (tileHeight + gutter)) + (tileHeight / 2) }
                                        })
                                        .text(function(d) { return "\u2613"; });
                                
                                    /****************/
                                    /***** ITEM *****/
                                    /****************/

                                    // set selection
                                    var shape = itemGroup
                                        .selectAll(".item")
                                        .data([row]);

                                    // enter selection
                                    shape
                                        .enter()
                                        .append("circle")
                                        .attr({
                                        class: "item"
                                    });

                                    // update selection
                                    shape
                                        .transition()
                                        .duration(1000)
                                        .attr({
                                            class: function(d) { 
                                                
                                                // corresponding circle pack item
                                                var cpEl = document.getElementById(d.name + "-cp");
                                                
                                                // check current state
                                                if (cpEl != null && cpEl.classList.contains("active")) {
                                                
                                                    // check for highlight
                                                    if (cpEl.classList.contains("highlight")) {
                                                        
                                                        return "item active highlight";
                                                        
                                                    } else {
                                                    
                                                        return "item active"; 
                                                        
                                                    };
                                                    
                                                } else {
                                                    
                                                    return "item";
                                                    
                                                };
                                            },
                                            id: function(d) { return d.name + "-hg-y"; },
                                            cx: 40, /* compute text length */
                                            cy: function(d, i) { return (rowIdx  * (tileHeight + gutter)) + (tileHeight / 2.16) },
                                            r: "0.15em" /* compute per font size */
                                        });
                                
                                })
                                .attr({
                                    class: "y-title"
                                });

                            // exit selection
                            column
                                .exit()
                                .remove();

                            /******************/
                            /***** X-AXIS *****/
                            /******************/

                            // set selection
                            var header = d3.select("#heat-x-header")
                                .selectAll("text")
                                .data(data[0].dates);

                            // enter selection
                            header
                                .enter()
                                .append("text");

                            // update selection
                            header
                                .style({
                                    opacity: 0
                                })
                                .attr({
                                    class: "x-axis",
                                    x: function(d, i) { return (i * (tileWidth + gutter)) + (tileWidth / 2) },
                                    y: (xLabelRow * height / 2) + 3, // calculate from css stroke width
                                })
                                .style({
                                    opacity: 1
                                })
                                .text(function(d, i) { 

                                    // get month digit
                                    var month = data[0].dates[i - 1];

                                    // need to just filter data out
                                    // this ensures the month isn't repeated over and over
                                    if (month == undefined) {

                                        // first instance of a month digit
                                        // and first date in grid
                                        //return moment(d.date).fromNow();

                                    } else if (month.date.split("-")[1] != d.date.split("-")[1]) {

                                        return moment(d.date).fromNow(); 

                                    };

                                });

                            // exit selection
                            header
                                .exit()
                                .remove();
                            
                            // add rule line
                            d3.select("#heat-x-header")
                                .append("line")
                                .attr({
                                    x1: 0,
                                    x2: activeXspace - (padding * 2),
                                    y1: 0,
                                    y2: 0
                                });

                        };
                        
                    };
                    
                });       
                
            });
            
        }
    }
    
}]);