angular.module("chord-diagram-directive", [])

.directive("chordDiagram", ["d3Service", function(d3Service){
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
                var height = parseInt(attrs.canvasHeight) || 400;
				
				// calculate values
				var outerRadius = width / 2;
				var bubbleRadius = innerRadius - 50;
				
				var innerRadius = .9 * outerRadius,
				linkRadius = .95 * innerRadius,
				nodesTranslate = outerRadius - innerRadius + (innerRadius - bubbleRadius),
				chordsTranslate = outerRadius,
				houseButton = d3.select(document.getElementById("houseButton")),
				senateButton = d3.select(document.getElementById("senateButton"));
				
				// set layouts
				var bubble = d3.layout.pack()
					.sort(null)
					.size([2 * bubbleRadius, 2 * bubbleRadius])
					.padding(1.5);
                                
                // create svg canvas
                var svg = d3.select(element[0])
                    .append("svg")
                    .attr({
                        viewBox: "0 0 " + width + " " + height
                    })
					.style({
						height: 2 * outerRadius + 200 + "px",
						width: 2 * outerRadius + 200 + "px"
					});
				
				// add group for arcs
				var linksSvg = svg
					.append("g")
					.attr({
						class: "links",
						transform: "translate(" + outerRadius + "," + outerRadius + ")"
					});
				
                // check for new data
                scope.$watch("vizData", function(newData, oldData) {
                    
                    // async check
                    //if (newData !== undefined) {
                    
                        // check new vs old
                        var isMatching = angular.equals(newData, oldData);

                        // if false
                        //if (!isMatching) {

                            // update the viz
                            draw(newData);

                        //};
                        
                        function draw(data) {
							
							var chordsById = {};
							var office = "house";
							var total_hDems = 0;
							var h_dems = [];
							var total_hReps = 0;
							var h_reps = [];
							var total_hOthers = 0;
							var h_others = [];
							var c_house = [];
							var pacs = [];
							
							//initialize();
							
							// select arc group
							/*var linkGroup = linksSvg
								.selectAll("g.links")
								.data(data, function(a, b) { return a.Key; });

							// enter selection
							var c = linkGroup
								.enter()
								.append("g")
								.attr("class", "links");

							//linkGroup.transition();

							// add arc
							c.append("g")
								.attr("class", "arc")
								.append("path")
								.attr({
									id: function(a) { return "a_" + a.Key; },
									d: function(a, b) {
										var c = {},
											d = chordsById[a.CMTE_ID];
										c.startAngle = d.currentAngle, d.currentAngle = d.currentAngle + Number(a.TRANSACTION_AMT) / d.value * (d.endAngle - d.startAngle), c.endAngle = d.currentAngle, c.value = Number(a.TRANSACTION_AMT);
										var e = d3.svg.arc(a, b).innerRadius(linkRadius).outerRadius(innerRadius);
										return totalContributions += c.value, total.text(formatCurrency(totalContributions)), e(c, b)
									}
								})
								.style({
									fill: function(a) { return "DEM" == a.PTY ? demColor : "REP" == a.PTY ? repColor : otherColor; },
									"fill-opacity": 0.2
								});*/
							
							
function log(a) {}

function node_onMouseOver(a, b) {
    var c = d3.event.pageX + 15;
    if (c + 250 > window.innerWidth && (c = d3.event.pageX - 280), "CAND" == b) {
        if (a.depth < 2) return;
        toolTip.transition().duration(200).style("opacity", ".9"), header1.text("Congress"), header.text(a.CAND_NAME), header2.text("Total Recieved: " + formatCurrency(Number(a.Amount))), toolTip.style("left", c + "px").style("top", d3.event.pageY - 150 + "px").style("height", "100px"), highlightLinks(a, !0)
    } else "CONTRIBUTION" == b ? (toolTip.transition().duration(200).style("opacity", ".9"), header1.text(pacsById[office + "_" + a.CMTE_ID].CMTE_NM), header.text(a.CAND_NAME), header2.text(formatCurrency(Number(a.TRANSACTION_AMT)) + " on " + a.Month + "/" + a.Day + "/" + a.Year), toolTip.style("left", c + "px").style("top", d3.event.pageY - 150 + "px").style("height", "100px"), highlightLink(a, !0)) : "PAC" == b && (toolTip.transition().duration(200).style("opacity", ".9"), header1.text("Political Action Committee"), header.text(pacsById[office + "_" + a.label].CMTE_NM), header2.text("Total Contributions: " + formatCurrency(pacsById[office + "_" + a.label].Amount)), toolTip.style("left", d3.event.pageX + 15 + "px").style("top", d3.event.pageY - 75 + "px").style("height", "110px"), highlightLinks(chordsById[a.label], !0))
}

function node_onMouseOut(a, b) {
    "CAND" == b ? highlightLinks(a, !1) : "CONTRIBUTION" == b ? highlightLink(a, !1) : "PAC" == b && highlightLinks(chordsById[a.label], !1), toolTip.transition().duration(500).style("opacity", "0")
}

function highlightLinks(a, b) {
    a.relatedLinks.forEach(function(a) {
        highlightLink(a, b)
    })
}

function fetchData() {
    dataCalls = [], 
		addStream("data/Candidates_House.csv", onFetchCandidatesHouse), // bubbles in center
		addStream("data/Contributions_House.csv", onFetchContributionsHouse), // connections
		addStream("data/Pacs_House.csv", onFetchPacsHouse), // outside ring
		startFetch()
}

function onFetchCandidatesHouse(a) {//console.log(a);
    for (var b = 0; b < a.length; b++) {
        var c = a[b];
        c.value = Number(c.Amount), cns[c.CAND_ID] = c, house.push(c), "REP" == c.PTY ? (h_reps.push(c), total_hReps += c.value) : "DEM" == c.PTY ? (h_dems.push(c), total_hDems += c.value) : (h_others.push(c), total_hOthers += c.value)
    }
    console.log("onFetchCandidatesHouse()"), endFetch()
}

function onFetchContributionsHouse(a) {
    var b = 0;
    a.forEach(function(a) {
        a.Key = "H" + b++, contributions.push(a), c_house.push(a)
    }), log("onFetchContributionsHouse()"), endFetch()
}

function onFetchPacsHouse(a) {
    pacsHouse = a;
    for (var b = 0; b < pacsHouse.length; b++) pacsById["house_" + pacsHouse[b].CMTE_ID] = pacsHouse[b];
    log("onFetchPacsHouse()"), endFetch()
}

function addStream(a, b) {
    var c = {};
    c.file = a, c["function"] = b, dataCalls.push(c)
}

function startFetch() {
    numCalls = dataCalls.length, 
		dataCalls.forEach(function(a) {
        d3.csv(a.file, a["function"])
    })
}

function endFetch() {
    numCalls--, 0 == numCalls && main()
}

function updateLinks(a) {
	//console.log(a);
    /*function b(a) {
        var b = {},
            c = {},
            d = {},
            e = {},
            f = {},
            g = chordsById[a.CMTE_ID],
            h = nodesById[a.CAND_ID],
            i = linkRadius,
            j = (i * Math.cos(g.currentLinkAngle - 1.57079633), i * Math.sin(g.currentLinkAngle - 1.57079633), g.currentLinkAngle - 1.57079633);
        g.currentLinkAngle = g.currentLinkAngle + Number(a.TRANSACTION_AMT) / g.value * (g.endAngle - g.startAngle);
        var k = g.currentLinkAngle - 1.57079633;
        return c.x = i * Math.cos(j), c.y = i * Math.sin(j), b.x = h.x - (chordsTranslate - nodesTranslate), b.y = h.y - (chordsTranslate - nodesTranslate), f.x = i * Math.cos(k), f.y = i * Math.sin(k), d.source = c, d.target = b, e.source = b, e.target = f, [d, e]
    };*/
	
    var linkGroup = linksSvg
		.selectAll("g.links")
		.data(a, function(a, b) { return a.Key; });
	
	// enter selection
    var c = linkGroup
		.enter()
		.append("g")
		.attr("class", "links");
	
    //linkGroup.transition();
	
	// add arc
    c.append("g")
		.attr("class", "arc")
		.append("path")
		.attr({
			id: function(a) { return "a_" + a.Key; },
			d: function(a, b) {
				var c = {},
					d = chordsById[a.CMTE_ID];
				c.startAngle = d.currentAngle, d.currentAngle = d.currentAngle + Number(a.TRANSACTION_AMT) / d.value * (d.endAngle - d.startAngle), c.endAngle = d.currentAngle, c.value = Number(a.TRANSACTION_AMT);
				var e = d3.svg.arc(a, b).innerRadius(linkRadius).outerRadius(innerRadius);
				return totalContributions += c.value, total.text(formatCurrency(totalContributions)), e(c, b)
			}
		})
		.style({
			fill: function(a) { return "DEM" == a.PTY ? demColor : "REP" == a.PTY ? repColor : otherColor; },
			"fill-opacity": 0.2
		})/*.on("mouseover", function(a) {
        node_onMouseOver(a, "CONTRIBUTION")
    }).on("mouseout", function(a) {
        node_onMouseOut(a, "CONTRIBUTION")
    }), c.append("path").attr("class", "link").attr("id", function(a) {
        return "l_" + a.Key
    }).attr("d", function(a, c) {
        a.links = b(a);
        var d = diagonal(a.links[0], c);
        return d += "L" + String(diagonal(a.links[1], c)).substr(1), d += "A" + linkRadius + "," + linkRadius + " 0 0,0 " + a.links[0].source.x + "," + a.links[0].source.y
    }).style("stroke", function(a) {
        return "DEM" == a.PTY ? demColor : "REP" == a.PTY ? repColor : otherColor
    }).style("stroke-opacity", .07).style("fill-opacity", .1).style("fill", function(a) {
        return "DEM" == a.PTY ? demColor : "REP" == a.PTY ? repColor : otherColor
    }).on("mouseover", function(a) {
        node_onMouseOver(a, "CONTRIBUTION")
    }).on("mouseout", function(a) {
        node_onMouseOut(a, "CONTRIBUTION")
    }), c.append("g").attr("class", "node").append("circle").style("fill", function(a) {
        return "DEM" == a.PTY ? demColor : "REP" == a.PTY ? repColor : otherColor
    }).style("fill-opacity", .2).style("stroke-opacity", 1).attr("r", function(a) {
        var b = nodesById[a.CAND_ID];
        b.currentAmount = b.currentAmount - Number(a.TRANSACTION_AMT);
        var c = (b.Amount - b.currentAmount) / b.Amount;
        return b.r * c
    }).attr("transform", function(a, b) {
        return "translate(" + a.links[0].target.x + "," + a.links[0].target.y + ")"
    }), linkGroup.exit().remove()*/
}

function updateNodes() {
    var a = nodesSvg.selectAll("g.node").data(cands, function(a, b) {
            return a.CAND_ID
        }),
        b = a.enter().append("g").attr("class", "node").attr("transform", function(a) {
            return "translate(" + a.x + "," + a.y + ")"
        });
    b.append("circle").attr("r", function(a) {
        return a.r
    }).style("fill-opacity", function(a) {
        return a.depth < 2 ? 0 : .05
    }).style("stroke", function(a) {
        return "DEM" == a.PTY ? demColor : "REP" == a.PTY ? repColor : otherColor
    }).style("stroke-opacity", function(a) {
        return a.depth < 2 ? 0 : .2
    }).style("fill", function(a) {
        return "DEM" == a.PTY ? demColor : "REP" == a.PTY ? repColor : otherColor
    });
    var c = b.append("g").attr("id", function(a) {
        return "c_" + a.CAND_ID
    }).style("opacity", 0);
    c.append("circle").attr("r", function(a) {
        return a.r + 2
    }).style("fill-opacity", 0).style("stroke", "#FFF").style("stroke-width", 2.5).style("stroke-opacity", .7), c.append("circle").attr("r", function(a) {
        return a.r
    }).style("fill-opacity", 0).style("stroke", "#000").style("stroke-width", 1.5).style("stroke-opacity", 1).on("mouseover", function(a) {
        node_onMouseOver(a, "CAND")
    }).on("mouseout", function(a) {
        node_onMouseOut(a, "CAND")
    }), a.exit().remove().transition(500).style("opacity", 0), console.log("updateBubble()")
}

function updateChords() {
    var a = chordsSvg.selectAll("g.arc").data(chords, function(a) {
            return a.label
        }),
        b = a.enter().append("g").attr("class", "arc"),
        c = defs.selectAll(".arcDefs").data(labelChords, function(a) {
            return a.label
        });
    c.enter().append("path").attr("class", "arcDefs").attr("id", function(a, b) {
        return "labelArc_" + a.label
    }), b.append("path").style("fill-opacity", 0).style("stroke", "#555").style("stroke-opacity", .4), b.append("text").attr("class", "chord").attr("id", function(a) {
        return "t_" + a.label
    }).on("mouseover", function(a) {
        node_onMouseOver(a, "PAC")
    }).on("mouseout", function(a) {
        node_onMouseOut(a, "PAC")
    }).style("font-size", "0px").style("fill", "#777").append("textPath").text(function(a) {
        return pacsById[office + "_" + a.label].CMTE_NM
    }).attr("text-anchor", "middle").attr("startOffset", "50%").style("overflow", "visible").attr("xlink:href", function(a, b) {
        return "#labelArc_" + a.label
    }), c.attr("d", function(a, b) {
        var c = d3.svg.arc().innerRadius(1.05 * innerRadius).outerRadius(1.05 * innerRadius)(a),
            d = /[Mm][\d\.\-e,\s]+[Aa][\d\.\-e,\s]+/,
            e = d.exec(c)[0];
        return e
    }), a.transition().select("path").attr("d", function(a, b) {
        var c = d3.svg.arc(a, b).innerRadius(.95 * innerRadius).outerRadius(innerRadius);
        return c(a.source, b)
    }), c.exit().remove(), a.exit().remove(), console.log("updateChords()")
}

function trimLabel(a) {
    return a.length > 25 ? String(a).substr(0, 25) + "..." : a
}

function getChordColor(a) {
    var b = nameByIndex[a];
    return void 0 == colorByName[b] && (colorByName[b] = fills(a)), colorByName[b]
}

function main() {
    initialize(), 
		//updateNodes(),  // draw the nodes
		//updateChords(), 
		intervalId = setInterval(onInterval, 1)
}

function onInterval() {
    if (0 == contr.length) clearInterval(intervalId);
    else {
        for (var a = 0; counter > a; a++) contr.length > 0 && renderLinks.push(contr.pop());
        counter = 30, updateLinks(renderLinks)
    }
}
							
var defs = svg.append("defs").append("g").attr("transform", "translate(" + chordsTranslate + "," + chordsTranslate + ")"),
    topMargin = .15 * innerRadius,
    chordsSvg = svg.append("g").attr("class", "chords").attr("transform", "translate(" + chordsTranslate + "," + (chordsTranslate + topMargin) + ")"),
    highlightSvg = svg.append("g").attr("transform", "translate(" + chordsTranslate + "," + (chordsTranslate + topMargin) + ")").style("opacity", 0),
    highlightLink = highlightSvg.append("path"),
    nodesSvg = svg.append("g").attr("class", "nodes").attr("transform", "translate(" + nodesTranslate + "," + (nodesTranslate + topMargin) + ")"),
    chord = d3.layout.chord().padding(.05).sortSubgroups(d3.descending).sortChords(d3.descending),
    diagonal = d3.svg.diagonal.radial(),
    arc = d3.svg.arc().innerRadius(innerRadius).outerRadius(innerRadius + 10),
    diameter = 960,
    format = d3.format(",d"),
    color = d3.scale.category20c(),
    toolTip = d3.select(document.getElementById("toolTip")),
    header = d3.select(document.getElementById("head")),
    header1 = d3.select(document.getElementById("header1")),
    header2 = d3.select(document.getElementById("header2")),
    total = d3.select(document.getElementById("totalDiv")),
    repColor = "#F80018",
    demColor = "#0543bc",
    otherColor = "#FFa400",
    fills = d3.scale.ordinal().range(["#00AC6B", "#20815D", "#007046", "#35D699", "#60D6A9"]),
    cns = [],
    cands = [],
    pacsHouse = [],
    pacsSentate = [],
    contr = [],
    house = [];

s_dems = [], s_reps = [], s_others = [], senate = [], total_sDems = 0, total_sReps = 0, total_sOthers = 0, contributions = [], c_senate = [], pacsById = {}, nodesById = {}, chordCount = 20, pText = null, pChords = null, nodes = [], renderLinks = [], colorByName = {}, totalContributions = 0, delay = 2;

var formatNumber = d3.format(",.0f"),
    formatCurrency = function(a) {
        return "$" + formatNumber(a)
    },
    buf_indexByName = {},
    indexByName = {},
    nameByIndex = {},
    labels = [],
    chords = [];

highlightLink = function(a, b) {
    var c = 1 == b ? .6 : .1,
        d = d3.select(document.getElementById("l_" + a.Key));
    d.transition(1 == b ? 150 : 550).style("fill-opacity", c).style("stroke-opacity", c);
    var e = d3.select(document.getElementById("a_" + a.Key));
    e.transition().style("fill-opacity", 1 == b ? c : .2);
    var f = d3.select(document.getElementById("c_" + a.CAND_ID));
    f.transition(1 == b ? 150 : 550).style("opacity", 1 == b ? 1 : 0);
    var g = d3.select(document.getElementById("t_" + a.CMTE_ID));
    g.transition(1 == b ? 0 : 550).style("fill", 1 == b ? "#000" : "#777").style("font-size", 1 == b ? Math.round(.035 * innerRadius) + "px" : "0px")
}, senateButton.on("click", function(a) {
    senateButton.attr("class", "selected"), houseButton.attr("class", null), office = "senate", linksSvg.selectAll("g.links").remove(), clearInterval(intervalId), main()
}), houseButton.on("click", function(a) {
    senateButton.attr("class", null), houseButton.attr("class", "selected"), office = "house", clearInterval(intervalId), main()
});
var dataCalls = [],
    numCalls = 0;
fetchData();
var intervalId, counter = 2,
    renderLinks = [];
							
							function initialize() {
								if (totalContributions = 0, renderLinks = [], cands = [], pacs = [], contr = [], "house" == office) {
									var a = {},
										b = {};
									b.value = total_hDems, b.children = h_dems;
									var c = {};
									c.value = total_hReps, c.children = h_reps;
									var d = {};
									d.value = total_hOthers, d.children = h_others, a.children = [c, b, d], a.PTY = "root", nodes = bubble.nodes(a);
									var e = 0;
									nodes.forEach(function(a) {
										2 == a.depth && (nodesById[a.CAND_ID] = a, a.relatedLinks = [], a.Amount = Number(a.Amount), a.currentAmount = a.Amount, cands.push(a), e += a.Amount)
									}), console.log("totalCandAmount=" + e), pacs = pacsHouse, c_house.forEach(function(a) {
										contr.push(a)
									})
								};
								buildChords();
								var f = 0;
								contr.forEach(function(a) {
									nodesById[a.CAND_ID].relatedLinks.push(a), chordsById[a.CMTE_ID].relatedLinks.push(a), f += Number(a.TRANSACTION_AMT)
								}), console.log("totalContributions=" + f), console.log("initialize()")
							};
							
							function buildChords() {
								console.log(pacs);
								var a = [];
								labels = [], chords = [], labelChords = [];
								for (var b = 0; b < pacs.length; b++) {
									var c = {};
									c.index = b, c.label = "null", c.angle = 0, labels.push(c);
									var d = {};
									d.label = "null", d.source = {}, d.target = {}, chords.push(d)
								}
								buf_indexByName = indexByName, indexByName = [], nameByIndex = [], n = 0;
								var e = 0;
								pacs.forEach(function(a) {
									a = a.CMTE_ID, a in indexByName || (nameByIndex[n] = a, indexByName[a] = n++)
								}), pacs.forEach(function(b) {
									var c = indexByName[b.CMTE_ID],
										d = a[c];
									if (!d) {
										d = a[c] = [];
										for (var f = -1; ++f < n;) d[f] = 0
									}
									d[indexByName[b.CMTE_ID]] = Number(b.Amount), e += Number(b.Amount)
								}), chord.matrix(a);
								chords = chord.chords();
								var f = 90 * Math.PI / 180,
									b = 0;
								chords.forEach(function(a) {
									a.label = nameByIndex[b], a.angle = (a.source.startAngle + a.source.endAngle) / 2;
									var c = {};
									c.startAngle = a.source.startAngle, c.endAngle = a.source.endAngle, c.index = a.source.index, c.value = a.source.value, c.currentAngle = a.source.startAngle, c.currentLinkAngle = a.source.startAngle, c.Amount = a.source.value, c.source = a.source, c.relatedLinks = [], chordsById[a.label] = c;
									var d = {};
									d.startAngle = a.source.startAngle - f / 2, d.endAngle = a.source.endAngle + f / 2, d.angle = a.angle + f, d.label = a.label, labelChords.push(d), b++
								}), console.log("buildChords()")
								
							};
							
						};
                        
                    //};
                    
                });       
                
            });
            
        }
    }
    
}]);