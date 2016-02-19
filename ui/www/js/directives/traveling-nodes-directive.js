angular.module("traveling-nodes-directive", [])

.directive("travelingNodes", ["d3Service", "dataService", "$stateParams", "$state", "$timeout", function(d3Service, dataService, $stateParams, $state, $timeout) {
	return {
		restrict: "E",
		scope: {
			vizData: "=",
            canvasWidth: "=",
            canvasHeight: "=",
            title: "="
		},
        template: "<img ng-src='{{ currentImg }}'/><p>{{ title }}</p>",
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
					.charge(0)
                    .gravity(0)
                    .friction(.9)
                    .size([(width - diameter), (height - diameter)]);
                
                var canvas = d3.select(element[0])
                    .append("svg")
                    .attr({
                        viewBox: "0 0 " + width + " " + height
                    });
                
                var nodes = d3.range(100).map(function(i) {
                  return {index: i};
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
                            
var USER_SPEED = "slow";

var padding = 0,
	maxRadius = 2;
	
var sched_objs = [],
	curr_minute = 0;

var act_codes = [
	{"index": "0", "short": "", "desc": ""},
	{"index": "1", "short": "", "desc": ""},
	{"index": "2", "short": "", "desc": ""},
	{"index": "3", "short": "", "desc": ""},
	{"index": "4", "short": "", "desc": "None"},
    {"index": "5", "short": "", "desc": ""},
    {"index": "6", "short": "", "desc": ""},
    {"index": "7", "short": "", "desc": ""},
    {"index": "8", "short": "", "desc": ""}
];


var speeds = { "slow": 1000, "medium": 200, "fast": 50 };


var time_notes = [
	{ "start_minute": 1, "stop_minute": 40, "note": "The simulation kicks in, based on data from the American Time Use Survey." },
	{ "start_minute": 70, "stop_minute": 120, "note": "Most people are still sleeping this early in the morning, but some are already at work or preparing for the day." },
	{ "start_minute": 180, "stop_minute": 300, "note": "It's wake up time for most. Time to start the day with morning rituals, breakfast and a wonderful commute." },
	{ "start_minute": 360, "stop_minute": 440, "note": "The day is in full swing with work or housework. Stores and services are open so people can run errands, and they take various forms of transportation to get there." },
	{ "start_minute": 480, "stop_minute": 540, "note": "Lunch hour. Many go eat, but there's still activity throughout. You see a small shift at the end of the hour." },
	{ "start_minute": 660, "stop_minute": 720, "note": "Coffee break? Again, at the top of the hour, you see a shift in activity." },
	{ "start_minute": 780, "stop_minute": 830, "note": "With the work day done, it's time to commute home and fix dinner or go out for a while." },
	{ "start_minute": 870, "stop_minute": 890, "note": "Dinner time!" },
	{ "start_minute": 930, "stop_minute": 1010, "note": "Dinner's done. Time for relaxation, TV, games, hobbies and socializing." },
	{ "start_minute": 1080, "stop_minute": 1140, "note": "Winding down for the day. From leisure time, people shift to personal care and sleep." },
	{ "start_minute": 1210, "stop_minute": 1300, "note": "Goodnight. More than 80% of people are asleep and it peaks at 96% around 3:00am." },
];
var notes_index = 0;


// Activity to put in center of circle arrangement
var center_act = "None",
	center_pt = { "x": 380, "y": 365 };


// Coordinates for clusters
var foci = {};
                            
act_codes.forEach(function(code, i) {
    
    // center point
	if (code.desc == center_act) {
		foci[code.index] = center_pt;
	} else {
		
        // check for left side row
        // clean up later into probably separate data sources
        
        if (i < (act_codes.length / 2)) {
            
            // set as row
            foci[code.index] = { x: (0 + radius), y: (height / (act_codes.length/2)) * i };
            
        } else {
            
            // set on right side
            foci[code.index] = { x: (width - radius), y: (height / (act_codes.length/2)) * (i - (act_codes.length/2)) };
            
        };
        
    };
        
});

// Load data and let's do it.
d3.tsv("data/test3.tsv", function(error, data) {
    
    var button = d3.select(element[0])
                    .append("button")
                    .text("steps")
                            .style({
                                position: "absolute",
                                top: '1em',
                                left: '1em'
                            })
                    .on("click", function() {
                        
                        var nodes = d3.selectAll(".node");
                        
                        // fix later w/state change
                        if (nodes[0][0]["__data__"].moves == 0) {
                            
                            scope.title = "Feature Extraction";
                            
                        } else if (nodes[0][0]["__data__"].moves == 1) {
                            
                            scope.title = "Clustering";
                            
                        } else if (nodes[0][0]["__data__"].moves == 2) {
                            
                            scope.title = "Classification";
                            
                        };
                        
                        // fix later with state check
                        if (nodes[0][0]["__data__"].moves < 3) {
                                                
                            nodes
                                .transition()
                                .duration(500)
                                .attr({
                                    rx: 0,
                                    ry: 0
                                });
                            
                        } else {
                            
                            nodes
                                .transition()
                                .duration(500)
                                .attr({
                                    rx: 5,
                                    ry: 5
                                });
                            
                        };
                        
                        d3.range(nodes[0].length).map(function(i) {
                        
                            var nodeD = nodes[0][i]["__data__"];// bad to use __data__ need to find better way to target
                            
                            // use global timer function to move nodes so force layout is maintained
                        timer(nodeD, nodes[0][i].parentNode);
    
                        });
                        
                        // make sure force is done before drawing feature set
                        force.on("end", function() {
                            
                            d3.range(nodes[0].length).map(function(i) {

                            // draw features chart
                            drawFeatures(nodes[0][i].parentNode);
                                
                            });

                        });
                        
                    });
	
	data.forEach(function(d) {
		var step_array = d.step.split(",");
		var activities = [];
        
        // loop through steps
		for (var i=0; i < step_array.length; i++) {
            
			// if index is odd == duration
			//if (i % 2 == 1) {
				activities.push({'act': step_array[i]});
			//};
            
		};
        
		sched_objs.push(activities);
	});
	
	// Used for percentages by minute
	var act_counts = { "0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0, "11": 0, "12": 0, "13": 0, "14": 0, "15": 0, "16": 0 };
	
	// A node for each doc's pathway
	var nodes = sched_objs.map(function(o,i) {
        
		var act = o[0].act; // starting step
		act_counts[act] += 1;
		var init_x = foci[act].x + Math.random(); // start out rando
		var init_y = foci[act].y + Math.random(); // start out rando
		return {
			act: act,
			radius: radius,
			x: init_x,
			y: init_y,
			color: color(act),
			moves: 0,
			next_move_time: o[0].duration,
			sched: o,
		}
	});
                                               
                                               
force
		.nodes(nodes)
        .on("tick", tick)
		.start();
	

	var group = canvas
        .selectAll("g")
		.data(nodes)
	  .enter()
        .append("g");
    
    var circle = group
        .append("rect")
		.attr({
            class: "node",
            height: radius,
            width: radius,
            rx: 5,
            ry: 5
                                })
		//.style("fill", function(d) { return d.color; })
        .on({
            click: function(d) {
                
                var nodeD = d;
                var elementSelect = this;
                
                // show image
                //scope.currentImg = "data/benchmarking/001_1.png"
                console.log("show doc feature extraction - heatmap?");
                
                // modify corner radius so now the shape looks like a square
                d3.select(this)
                    .transition()
                    .duration(500)
                    .attr({
                        rx: 0,
                        ry: 0
                    })
                    .style({
                        fill: "transparent",
                        stroke: "red"
                    });
                
                // use global timer function to move nodes so force layout is maintained
                timer(nodeD, elementSelect.parentNode);
                
                // make sure force is done before drawing feature set
                force.on("end", function() {
                    
                    // draw features chart
                    drawFeatures(elementSelect.parentNode);
                    
                });
                
            }
        });
    
    function drawFeatures(parent) {
                                    
                var data = [
                    {
                        name: "feature",
                        value: 5
                    },
                    {
                        name: "feature",
                        value: 8
                    },
                    {
                        name: "feature",
                        value: 200
                    },
                    {
                        name: "feature",
                        value: 90
                    },
                    {
                        name: "feature",
                        value: 9
                    },
                    {
                        name: "feature",
                        value: 5
                    }
                ];
        
        var docNode2 = d3.select(parent)
            .select(".node");
        console.log(docNode2[0][0]["__data__"].moves);
        // really bad way to select
        // need to fix
        if (docNode2[0][0]["__data__"].moves > 3) {
            
            // hacky way to remove
            // fix later
            d3.select(parent)
                .select(".feature")
                .remove();
            
        } else {
            
            var xAxisHeight = (0.3 * height);// % of total canvas height
                var activeHeight = height - xAxisHeight - (padding * 2);
                var activeWidth = width - (padding * 2);
                                var colorRange = ["white", "grey"];
                                // set up stack layout
                var stack = d3.layout.stack();
                
                
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
                            
                            // set selection
                            var bar = d3.select(parent)
                                .selectAll(".feature")
                                .data(data);
        
        // update selection
        bar
            .transition()
            .duration(500)
            .attr({
                class: "feature",
                x: function(d) { return xScale(d[0].x0); },
                y: 0,
                height: 10,
                width: function(d) { return xScale(d[0].x); }
            })
            .style({
                fill: function(d) { return colorScale(d[0].value); }
            });
        
                                // enter selection
                                bar
                                .enter()
                                .append("rect")
                                .transition()
                                    .duration(500)
                                .attr({
                                    class: "feature",
                                    x: function(d) { return xScale(d[0].x0); },
                                    y: 0,
                                    height: 10,
                                    width: function(d) { return xScale(d[0].x); }
                                })
                                .style({
                                    fill: function(d) { return colorScale(d[0].value); }
                                });
        
        // exit selection
        bar
            .exit()
            .transition()
            .duration(500)
            .remove();
                                         
                };
        
        };
                                
	
	// Activity labels
	var label = canvas.selectAll("text")
		.data(act_codes)
	  .enter().append("text")
		.attr("class", "actlabel")
		.attr("x", function(d, i) {
			if (d.desc == center_act) {
				return center_pt.x;
			} else {
				var theta = 2 * Math.PI / (act_codes.length-1);
				return 340 * Math.cos(i * theta)+380;
			}
			
		})
		.attr("y", function(d, i) {
			if (d.desc == center_act) {
				return center_pt.y;
			} else {
				var theta = 2 * Math.PI / (act_codes.length-1);
				return 340 * Math.sin(i * theta)+365;
			}
			
		});
		
	label.append("tspan")
		.attr("x", function() { return d3.select(this.parentNode).attr("x"); })
		// .attr("dy", "1.3em")
		.attr("text-anchor", "middle")
		.text(function(d) {return "";
			//return d.short;
		});
	label.append("tspan")
		.attr("dy", "1.3em")
		.attr("x", function() { return d3.select(this.parentNode).attr("x"); })
		.attr("text-anchor", "middle")
		.attr("class", "actpct")
		.text(function(d) {return "";
			//return act_counts[d.index] + "%";
		});
		

	// Update nodes based on activity and duration
	function timer(cNode, parentElement) {
		//d3.range(nodes.length).map(function(i) {
			//var curr_node = nodes[i];
            var curr_node = cNode;
				curr_moves = curr_node.moves; 

			// Time to go to next step
			//if (curr_node.next_move_time == curr_minute) {
				if (curr_node.moves == curr_node.sched.length-1) {
					curr_moves = 0;
				} else {
					curr_moves += 1;
				}
			
				// Subtract from current activity count
				act_counts[curr_node.act] -= 1;
			
				// Move on to next activity
				curr_node.act = curr_node.sched[ curr_moves ].act;
			
				// Add to new activity count
				act_counts[curr_node.act] += 1;
			
				curr_node.moves = curr_moves;
        
        
				//curr_node.cx = foci[curr_node.act].x;
				//curr_node.cy = foci[curr_node.act].y;
       
                    d3.select(parentElement)
                      //.each(collide(.5))
                      //.style("fill", function(d) { return d.color; })
                      .attr({
                      transform: "translate(" + foci[curr_node.act].x + "," + foci[curr_node.act].y + ")"
                  });
			
				//nodes[i].next_move_time += nodes[i].sched[ curr_node.moves ].duration;

			//}

		//});

		force.resume()
		curr_minute += 1;
/*
		// Update percentages
		label.selectAll("tspan.actpct")
			.text(function(d) {
				return readablePercent(act_counts[d.index]);
			});
	
		// Update time
		var true_minute = curr_minute % 1440;
		d3.select("#current_time").text(minutesToTime(true_minute));
		
		// Update notes
		// var true_minute = curr_minute % 1440;
		if (true_minute == time_notes[notes_index].start_minute) {
			d3.select("#note")
				.style("top", "0px")
			  .transition()
				.duration(600)
				.style("top", "20px")
				.style("color", "#000000")
				.text(time_notes[notes_index].note);
		} 
		
		// Make note disappear at the end.
		else if (true_minute == time_notes[notes_index].stop_minute) {
			
			d3.select("#note").transition()
				.duration(1000)
				.style("top", "300px")
				.style("color", "#ffffff");
				
			notes_index += 1;
			if (notes_index == time_notes.length) {
				notes_index = 0;
			}
		}
		*/
		
		//setTimeout(timer, speeds[USER_SPEED]);
	}
	//setTimeout(timer, speeds[USER_SPEED]);
	
	
	
		
	function tick(e) {
	  var k = 0.04 * e.alpha;
  
	  // Push nodes toward their designated focus.
	  nodes.forEach(function(o, i) {
		var curr_act = o.act;
		
		// Make sleep more sluggish moving.
		if (curr_act == "0") {
			var damper = 0.6;
		} else {
			var damper = 1;
		}
		o.color = color(curr_act);
	    o.y += (foci[curr_act].y - o.y) * k * damper;
	    o.x += (foci[curr_act].x - o.x) * k * damper;
	  });

	  group
	  	  .each(collide(.5))
	  	  //.style("fill", function(d) { return d.color; })
	      .attr({
          transform: function(d) { return "translate(" + d.x + "," + d.y + ")"; }
      });
	}


	// Resolve collisions between nodes.
	function collide(alpha) {
	  var quadtree = d3.geom.quadtree(nodes);
	  return function(d) {
	    var r = d.radius + maxRadius + padding,
	        nx1 = d.x - r,
	        nx2 = d.x + r,
	        ny1 = d.y - r,
	        ny2 = d.y + r;
	    quadtree.visit(function(quad, x1, y1, x2, y2) {
	      if (quad.point && (quad.point !== d)) {
	        var x = d.x - quad.point.x,
	            y = d.y - quad.point.y,
	            l = Math.sqrt(x * x + y * y),
	            r = d.radius + quad.point.radius + (d.act !== quad.point.act) * padding;
	        if (l < r) {
	          l = (l - r) / l * alpha;
	          d.x -= x *= l;
	          d.y -= y *= l;
	          quad.point.x += x;
	          quad.point.y += y;
	        }
	      }
	      return x1 > nx2 || x2 < nx1 || y1 > ny2 || y2 < ny1;
	    });
	  };
	}
	
	
	
	
	// Speed toggle
	d3.selectAll(".togglebutton")
      .on("click", function() {
        if (d3.select(this).attr("data-val") == "slow") {
            d3.select(".slow").classed("current", true);
			d3.select(".medium").classed("current", false);
            d3.select(".fast").classed("current", false);
        } else if (d3.select(this).attr("data-val") == "medium") {
            d3.select(".slow").classed("current", false);
			d3.select(".medium").classed("current", true);
            d3.select(".fast").classed("current", false);
        } 
		else {
            d3.select(".slow").classed("current", false);
			d3.select(".medium").classed("current", false);
			d3.select(".fast").classed("current", true);
        }
		
		USER_SPEED = d3.select(this).attr("data-val");
    });
}); // @end d3.tsv



function color(activity) {
	
	var colorByActivity = {
		"0": "#e0d400",
		"1": "#1c8af9",
		"2": "#51BC05",
		"3": "#FF7F00",
		"4": "#DB32A4",
		"5": "#00CDF8",
		"6": "#E63B60",
		"7": "#8E5649",
		"8": "#68c99e",
		"9": "#a477c8",
		"10": "#5C76EC",
		"11": "#E773C3",
		"12": "#799fd2",
		"13": "#038a6c",
		"14": "#cc87fa",
		"15": "#ee8e76",
		"16": "#bbbbbb",
	}
	return "black";
	//return colorByActivity[activity];
	
}



// Output readable percent based on count.
function readablePercent(n) {
	
	var pct = 100 * n / 1000;
	if (pct < 1 && pct > 0) {
		pct = "<1%";
	} else {
		pct = Math.round(pct) + "%";
	}
	
	return pct;
}


// Minutes to time of day. Data is minutes from 4am.
function minutesToTime(m) {
	var minutes = (m + 4*60) % 1440;
	var hh = Math.floor(minutes / 60);
	var ampm;
	if (hh > 12) {
		hh = hh - 12;
		ampm = "pm";
	} else if (hh == 12) {
		ampm = "pm";
	} else if (hh == 0) {
		hh = 12;
		ampm = "am";
	} else {
		ampm = "am";
	}
	var mm = minutes % 60;
	if (mm < 10) {
		mm = "0" + mm;
	}
	
	return hh + ":" + mm + ampm
}



                                
                        };
                        
                    };
                    
                });
				
			});
			
		}
		
	};
}]);