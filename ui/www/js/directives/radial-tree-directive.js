angular.module("radial-tree-directive", [])

.directive("radialTree", ["d3Service", function(d3Service){
    return {
        restrict: "E",
        scope: {
            vizData: "="
        },
        link: function(scope, element, attrs){
            
            //get d3 promise
            d3Service.d3().then(function(d3) {
				
                //bind data
                scope.$watch("vizData", function(newData, oldData) {
                    
                    //check for data
                    if (newData) {
                        
						var diameter = 960;

						var tree = d3.layout.tree()
							.size([360, ((diameter * 0.8) / 2 - 120)])
							.separation(function(a, b) { return (a.parent == b.parent ? 1 : 2) / a.depth; });

						var diagonal = d3.svg.diagonal.radial()
							.projection(function(d) { return [d.y, d.x / 180 * Math.PI]; });

						var svg = d3.select(element[0])
							.append("svg")
							.attr({
								viewBox: "0 0 " + diameter + " " + (diameter - 150)
							})
						  .append("g")
							.attr("transform", "translate(" + diameter / 2 + "," + diameter / 2 + ")");

						  var nodes = tree.nodes(newData),
							  links = tree.links(nodes);

						  var link = svg.selectAll(".link")
							  .data(links)
							.enter().append("path")
							  .attr("class", "link")
							  .attr("d", diagonal)
                                .style({
                                    stroke: function(d) {
                                        
                                        switch (d.source.return) {
                                            case true: return "#24f808";
                                            //case "attr": return "#24f808";
                                            //case "location": return "#d45b01";
                                            default: return "#a39f9f";
                                        }
                                    }
                                })

						  var node = svg.selectAll(".node")
							  .data(nodes)
							.enter().append("g")
							  .attr("class", "node")
							  .attr("transform", function(d) { return "rotate(" + (d.x - 90) + ")translate(" + d.y + ")"; })

						  /*node.append("circle")
							  .attr("r", 4.5)
                            .style({
                              fill: function(d) {
                                        
                                        switch (d.type) {
                                            case "param": return "none";
                                            case "attr": return "#24f808";
                                            case "obj": return "none";
                                            default: return "none";
                                        }
                                    }
                          });*/

						  node.append("text")
							  .attr("dy", ".31em")
							  .attr("text-anchor", function(d) { return d.x < 180 ? "start" : "end"; })
							  .attr("transform", function(d) { return d.x < 180 ? "translate(8)" : "rotate(180)translate(-8)"; })
							  .text(function(d) { return d.name; })
                                .style({
                              "display": function(d) { return d.type == "obj" ? "none" : "inherit"; },
                                "font-size": function(d) { return d.type == "root" ? "2em" : "inherit"},
                              "font-weight": function(d) { return d.type == "param" ? "700" : "inherit"; }
                              });
                        
                        function elbow(d, i) {
  return "M" + d.source.y + "," + d.source.x
      + "V" + d.target.x + "H" + d.target.y;
}
                        
                    };
                    
                });       
                
            });
            
        }
    }
    
}]);