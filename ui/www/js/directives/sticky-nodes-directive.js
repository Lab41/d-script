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
				/*var width = parseInt(attrs.canvasWidth) || 700;
                var height = parseInt(attrs.canvasHeight) || width;
                var radius = 2;
                var diameter = radius * 2;
				var color = ["orange", "teal", "grey", "#5ba819"];
				
				var force = d3.layout.force()
					.charge(-10)
                    .linkDistance(20)
					//.linkDistance(function(d) { return d.value; })
                    .size([(width - diameter), (height - diameter)])
					//.on("tick", tick);

				/*var drag = force.drag()
					.on("dragstart", dragstart);*/

                // create svg canvas
                /*var canvas = d3.select(element[0])
                    .append("svg")
                    .attr({
                        viewBox: "0 0 " + width + " " + height
                    });
				
				//var link = canvas.selectAll(".link");
    			//var node = canvas.selectAll(".node");*/
                
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
                            //draw(newData);
                            
                            pixiDraw(newData);

                        };
                        
                        function draw(data) {

                            // set layout data
							force
							  .nodes(data.nodes)
							  .links(data.links)
							  .start();

						  /*link = link.data(data.links)
							.enter().append("line")
							  .attr("class", "link");
                            
                            node = node.data(force.nodes());
                          
                            
                            node.enter().append("circle").attr("class", function(d) { return "node " + d.id; }).attr("r", radius);
                          
                            // events
                            node.on({
                                click: function(d) {
                                    
                                    // show features
                                    d3.selectAll(".feature")
                                        .style({
                                            opacity: function(d) { return (d[0].value / 10); },
                                            fill: function(d, i) { return d[0].value > 9 ? "#e9f55c" : "currentColor"; }
                                        });
                                }
                            })
                            
                            node.exit().remove();*/
                            
                            var link = canvas
                                .selectAll(".link")
                                .data(data.links)
                                .enter()
                                .append("line")
                                .attr({
                                    class: "link"
                                })
                            
                            var node = canvas
                                .selectAll(".node")
                                .data(data.nodes)
                                .enter()
                                .append("circle")
                                .attr({
                                    class: "node",
                                    r: radius
                                })
                            
                            // events
                            node
                                .on({
                                click: function(d) {
                                    
                                    // make node active
                                    // figure out how to make element work with SVG
                                    //angular.element(this).toggleClass = "active";
                                    
                                    var isActive = d3.select(this).attr("class") == "node active" ? true : false;
                                    
                                    // check class
                                    if (isActive) {
                                        
                                        // make inactive
                                        d3.select(this)
                                            .attr({
                                                class: "node"
                                            });
                                        
                                    } else {
                                        
                                        // make active
                                        d3.select(this)
                                            .attr({
                                                class: "node active"
                                            });
                                        
                                    };
                                    
                                    // get attribute data for individual node
                                    dataService.getData("classification", d.id).then(function(data) {
                                        
                                        var vizScope = scope.$parent;
                        
                                        // assign to scope
                                        vizScope.details = [data].concat(vizScope.details);

                                    });
                                                                        
                                }
                            })
                                //.call(force.drag);
                            
                            force
                                .on("tick", function() {
                                
                                link.attr("x1", function(d) { return d.source.x; })
                                    .attr("y1", function(d) { return d.source.y; })
                                    .attr("x2", function(d) { return d.target.x; })
                                    .attr("y2", function(d) { return d.target.y; });
                                        
                                        node.attr("cx", function(d) { return d.x; })
                                            .attr("cy", function(d) { return d.y; });
                                        
                                    }
                                )
							
                        };
                        
                        function pixiDraw(data) {
                            
                            var dataNodes = data.nodes.length;
                            
                            // get size of available html container
                            var height = parseFloat(window.getComputedStyle(element[0].parentElement, null).height.split("px")[0]);
                            var width = parseFloat(window.getComputedStyle(element[0].parentElement, null).width.split("px")[0]);
                            /*
                            // create the renderer
                            var renderer = PIXI.autoDetectRenderer(width,height);
                           
                            // add canvas
                            element.append(renderer.view);
                            
                            // create stage container
                            var stage = new PIXI.Container();
                            
                            // render it real good
                            renderer.render(stage);*/
                            
                                  // First we setup PIXI for rendering:
      var stage = new PIXI.Container();
      stage.interactive = true;

      var renderer = PIXI.autoDetectRenderer(width, height, null, false, true);
      renderer.view.style.display = "block";
                            renderer.backgroundColor = 0xd4d4d4;
      element.append(renderer.view);

      var graphics = new PIXI.Graphics();
      graphics.position.x = width/2;
      graphics.position.y = height/2;
      graphics.scale.x = 0.2;
      graphics.scale.y = 0.2;
      stage.addChild(graphics);

      // Second, we create a graph and force directed layout
      //var graph = ngraph.createGraph.grid(Math.floor(Math.sqrt(dataNodes)), Math.floor(Math.sqrt(dataNodes)));
                            var graph = ngraph.graph();
      /*var simulator = ngraph.physics({
        springLength: 30,
        springCoeff: 0.0008,
        dragCoeff: 0.01,
        gravity: -1.2,
        theta: 1
      });*/
                            var dataLinks = [{"source": 0, "target": 1, "value": 90.972516688518382}, {"source": 0, "target": 2, "value": 95.029728116083035}, {"source": 0, "target": 3, "value": 92.48563765147253}, {"source": 0, "target": 4, "value": 90.61132145038124}, {"source": 0, "target": 5, "value": 93.374181697235485}, {"source": 0, "target": 6, "value": 92.067467118838863}, {"source": 0, "target": 7, "value": 94.866496318853052}, {"source": 0, "target": 8, "value": 98.002233924758912}, {"source": 0, "target": 9, "value": 96.970341744654078}, {"source": 0, "target": 10, "value": 99.755657421762095}, {"source": 0, "target": 11, "value": 107.82598015018257}, {"source": 0, "target": 12, "value": 95.457065786230004}, {"source": 0, "target": 13, "value": 94.443441982705025}, {"source": 0, "target": 14, "value": 99.189007787461975}, {"source": 0, "target": 15, "value": 101.21970957344163}, {"source": 0, "target": 16, "value": 91.097987141492652}, {"source": 0, "target": 17, "value": 94.957916065149377}, {"source": 0, "target": 18, "value": 96.284979530402751}, {"source": 0, "target": 19, "value": 97.888570203179626}, {"source": 0, "target": 20, "value": 88.334940491108839}, {"source": 0, "target": 21, "value": 91.226845811422365}, {"source": 0, "target": 22, "value": 92.751869171685414}, {"source": 0, "target": 23, "value": 91.711469718087784}, {"source": 0, "target": 24, "value": 89.868610226828849}, {"source": 0, "target": 25, "value": 90.734224147020512}, {"source": 0, "target": 26, "value": 95.971140135935897}, {"source": 0, "target": 27, "value": 94.696161615113283}, {"source": 0, "target": 28, "value": 88.16718963894823}, {"source": 0, "target": 29, "value": 90.599248077921203}, {"source": 0, "target": 30, "value": 88.530767113485609}, {"source": 0, "target": 31, "value": 88.414654057459217}, {"source": 0, "target": 32, "value": 88.847890252761616}, {"source": 0, "target": 33, "value": 90.539775841797038}, {"source": 0, "target": 34, "value": 92.532626900933451}, {"source": 0, "target": 35, "value": 93.215105445812341}, {"source": 0, "target": 36, "value": 97.190811219718213}, {"source": 0, "target": 37, "value": 98.282682503993527}, {"source": 0, "target": 38, "value": 105.69219253696164}, {"source": 0, "target": 39, "value": 104.70711412107832}, {"source": 0, "target": 40, "value": 102.85834294607329}, {"source": 0, "target": 41, "value": 110.47584619422089}, {"source": 0, "target": 42, "value": 106.51742138649551}, {"source": 0, "target": 43, "value": 105.99040230285742}, {"source": 0, "target": 44, "value": 97.992136147416829}, {"source": 0, "target": 45, "value": 91.08886880009517}, {"source": 0, "target": 46, "value": 99.421405923859567}, {"source": 0, "target": 47, "value": 100.44808183737949}, {"source": 0, "target": 48, "value": 106.88751422022973}, {"source": 0, "target": 49, "value": 113.39321645195207}, {"source": 0, "target": 50, "value": 113.59002623684592}, {"source": 0, "target": 51, "value": 117.64433044573357}, {"source": 0, "target": 52, "value": 104.83412406965928}, {"source": 0, "target": 53, "value": 109.67920307250368}, {"source": 0, "target": 54, "value": 108.60867024337878}, {"source": 0, "target": 55, "value": 112.37842191660916}, {"source": 0, "target": 56, "value": 91.18444074486996}, {"source": 0, "target": 57, "value": 92.364635089962022}, {"source": 0, "target": 58, "value": 89.139102420275847}, {"source": 0, "target": 59, "value": 89.194753558222786}, {"source": 0, "target": 60, "value": 103.52115619047896}, {"source": 0, "target": 61, "value": 107.39129117845329}, {"source": 0, "target": 62, "value": 118.48436671349567}, {"source": 0, "target": 63, "value": 120.86736552524458}, {"source": 0, "target": 64, "value": 91.212383116593472}, {"source": 0, "target": 65, "value": 92.757212479529301}, {"source": 0, "target": 66, "value": 95.953063236960716}, {"source": 0, "target": 67, "value": 94.108933816748646}, {"source": 0, "target": 68, "value": 89.447736286401167}, {"source": 0, "target": 69, "value": 91.849047652075356}, {"source": 0, "target": 70, "value": 94.246113431275987}, {"source": 0, "target": 71, "value": 94.387870083505447}, {"source": 0, "target": 72, "value": 95.084942861961324}, {"source": 0, "target": 73, "value": 95.5905576090518}, {"source": 0, "target": 74, "value": 98.33344633106401}, {"source": 0, "target": 75, "value": 98.50526827598091}, {"source": 0, "target": 76, "value": 94.802469190557431}, {"source": 0, "target": 77, "value": 97.878674336982954}, {"source": 0, "target": 78, "value": 98.855324335743447}, {"source": 0, "target": 79, "value": 102.39538275342544}, {"source": 0, "target": 80, "value": 97.517658217298461}, {"source": 0, "target": 81, "value": 97.454171697597374}, {"source": 0, "target": 82, "value": 96.527342699437767}, {"source": 0, "target": 83, "value": 105.88943490430536}, {"source": 0, "target": 84, "value": 89.181914360500741}, {"source": 0, "target": 85, "value": 90.557512412779772}, {"source": 0, "target": 86, "value": 92.254778353298164}, {"source": 0, "target": 87, "value": 94.408573593639531}, {"source": 0, "target": 88, "value": 90.239968817547719}, {"source": 0, "target": 89, "value": 91.973290760723373}, {"source": 0, "target": 90, "value": 91.543745408044771}, {"source": 0, "target": 91, "value": 89.68745833556865}, {"source": 0, "target": 92, "value": 93.219830458827573}, {"source": 0, "target": 93, "value": 96.620127094726044}, {"source": 0, "target": 94, "value": 95.798064606903466}, {"source": 0, "target": 95, "value": 98.334170990810307}, {"source": 0, "target": 96, "value": 90.712913634194436}, {"source": 0, "target": 97, "value": 92.052727035613174}, {"source": 0, "target": 98, "value": 89.070260881829086}, {"source": 0, "target": 99, "value": 94.2594264084222}, {"source": 0, "target": 100, "value": 94.861211884090579}, {"source": 0, "target": 101, "value": 95.303230055797698}, {"source": 0, "target": 102, "value": 99.197812215046028}, {"source": 0, "target": 103, "value": 102.6858826918799}, {"source": 0, "target": 104, "value": 101.60495211295822}, {"source": 0, "target": 105, "value": 105.58191024619069}, {"source": 0, "target": 106, "value": 106.21869753447717}, {"source": 0, "target": 107, "value": 107.37330737604003}, {"source": 0, "target": 108, "value": 90.336060638220516}, {"source": 0, "target": 109, "value": 93.348380832512177}, {"source": 0, "target": 110, "value": 95.154098818431706}, {"source": 0, "target": 111, "value": 95.20192132333122}, {"source": 0, "target": 112, "value": 101.61155293205645}, {"source": 0, "target": 113, "value": 103.21112662365358}, {"source": 0, "target": 114, "value": 106.13116078442194}, {"source": 0, "target": 115, "value": 106.59594679958245}, {"source": 0, "target": 116, "value": 96.904783053006923}, {"source": 0, "target": 117, "value": 99.650675977744797}, {"source": 0, "target": 118, "value": 99.839485471017426}, {"source": 0, "target": 119, "value": 105.59111202049435}, {"source": 0, "target": 120, "value": 97.676363356249311}, {"source": 0, "target": 121, "value": 103.83232281989031}, {"source": 0, "target": 122, "value": 104.13913054299505}, {"source": 0, "target": 123, "value": 108.48276615435773}, {"source": 0, "target": 124, "value": 97.195292334506092}, {"source": 0, "target": 125, "value": 102.9097325497285}, {"source": 0, "target": 126, "value": 98.572413225004624}, {"source": 0, "target": 127, "value": 107.73887578771598}, {"source": 0, "target": 128, "value": 102.86865171166411}, {"source": 0, "target": 129, "value": 106.31760322184751}, {"source": 0, "target": 130, "value": 107.02275551888275}, {"source": 0, "target": 131, "value": 107.02115868327712}, {"source": 0, "target": 132, "value": 96.483403890279774}, {"source": 0, "target": 133, "value": 99.976838626842905}, {"source": 0, "target": 134, "value": 102.63912758105049}, {"source": 0, "target": 135, "value": 105.49851970009627}, {"source": 0, "target": 136, "value": 104.91671462206041}, {"source": 0, "target": 137, "value": 103.72431704038311}, {"source": 0, "target": 138, "value": 104.7455385936014}, {"source": 0, "target": 139, "value": 113.36733078939966}, {"source": 0, "target": 140, "value": 106.61642990447496}, {"source": 0, "target": 141, "value": 103.1829779222184}, {"source": 0, "target": 142, "value": 102.66530774697735}, {"source": 0, "target": 143, "value": 101.79101579070797}, {"source": 0, "target": 144, "value": 85.901309614142278}, {"source": 0, "target": 145, "value": 92.413770506802138}, {"source": 0, "target": 146, "value": 90.427477248969936}, {"source": 0, "target": 147, "value": 89.887039529449368}, {"source": 0, "target": 148, "value": 91.768441419944836}, {"source": 0, "target": 149, "value": 95.897404000671671}, {"source": 0, "target": 150, "value": 99.659075656313888}, {"source": 0, "target": 151, "value": 99.485182132577762}, {"source": 0, "target": 152, "value": 97.825006250626515}, {"source": 0, "target": 153, "value": 101.42276818445758}, {"source": 0, "target": 154, "value": 99.898815381339091}, {"source": 0, "target": 155, "value": 97.734436116935612}, {"source": 0, "target": 156, "value": 101.55114338410543}, {"source": 0, "target": 157, "value": 104.33960359224008}, {"source": 0, "target": 158, "value": 112.58333098938819}, {"source": 0, "target": 159, "value": 117.04944544653594}, {"source": 0, "target": 160, "value": 103.76966880402416}, {"source": 0, "target": 161, "value": 102.76198139398744}, {"source": 0, "target": 162, "value": 104.4059846815836}, {"source": 0, "target": 163, "value": 106.20916308764154}, {"source": 0, "target": 164, "value": 91.126166073000277}, {"source": 0, "target": 165, "value": 93.821812580280607}, {"source": 0, "target": 166, "value": 98.892328395450406}, {"source": 0, "target": 167, "value": 101.26292844340789}, {"source": 0, "target": 168, "value": 90.209819228612346}, {"source": 0, "target": 169, "value": 93.088858711550259}, {"source": 0, "target": 170, "value": 100.15143486131747}, {"source": 0, "target": 171, "value": 96.288739780271897}, {"source": 0, "target": 172, "value": 100.44170815763093}, {"source": 0, "target": 173, "value": 103.78499286817562}, {"source": 0, "target": 174, "value": 113.08807384748046}, {"source": 0, "target": 175, "value": 110.87904781674106}, {"source": 0, "target": 176, "value": 101.29514547168225}, {"source": 0, "target": 177, "value": 102.6229652675022}, {"source": 0, "target": 178, "value": 104.387444167219}, {"source": 0, "target": 179, "value": 106.56528332979605}, {"source": 0, "target": 180, "value": 83.715929319845785}, {"source": 0, "target": 181, "value": 89.936081131093061}, {"source": 0, "target": 182, "value": 94.428484670624727}, {"source": 0, "target": 183, "value": 93.490771269797818}, {"source": 0, "target": 184, "value": 88.444965276420945}, {"source": 0, "target": 185, "value": 91.470966606402399}];
                            
                            // add nodes
                            angular.forEach(data.nodes, function(value, key) {
                                
                                graph.addNode(value.id, {
                                    info: 'these key/values go in data',
                                });
                                                                
                            });
                            
                            // add links
                            angular.forEach(dataLinks, function(value, key) {
                                
                                // add links
                                graph.addLink(data.nodes[value.source], data.nodes[value.target]);
                                
                            })

      var layout = ngraph.layout(graph/*, simulator*/);

      // Store node and link positions into arrays for quicker access within
      // animation loop:
      var nodePositions = [],
          linkPositions = [];
// node should be id, links, data
      graph.forEachNode(function(node) {//console.log(node);
        nodePositions.push(layout.getNodePosition(node.id));
      });
console.log(nodePositions[0].constructor.name);
      graph.forEachLink(function(link) {//console.log(link);
        linkPositions.push(layout.getLinkPosition(link.id));
      });

      // Finally launch animation loop:
      requestAnimationFrame(animate);

      function animate() {
        layout.step();
        drawGraph(graphics, nodePositions, linkPositions);
        renderer.render(stage);
        requestAnimationFrame(animate);
      }

      function drawGraph(graphics, nodePositions, linkPositions) {
        // No magic at all: Iterate over positions array and render nodes/links
        graphics.clear();
        graphics.beginFill(0x232222);
        var i, x, y, x1, y1;

        graphics.lineStyle(1, 0x232222, 1);
          
        for(i = 0; i < linkPositions.length; ++i) {
          var link = linkPositions[i];
          graphics.moveTo(link.from.x, link.from.y);
          graphics.lineTo(link.to.x, link.to.y);
        }

          // nodes
        graphics.lineStyle(0);
          
        for (i = 0; i < nodePositions.length; ++i) {
          x = nodePositions[i].x - 5;
          y = nodePositions[i].y - 5;
          graphics.drawCircle(x, y, 4);
        }
      }
                            
                        }
                        
                    };
                    
                });
				
				/*function tick() {
				  link.attr("x1", function(d) { return d.source.x; })
					  .attr("y1", function(d) { return d.source.y; })
					  .attr("x2", function(d) { return d.dest.x; })
					  .attr("y2", function(d) { return d.dest.y; });

				  node.attr("cx", function(d) { return d.x; })
					  .attr("cy", function(d) { return d.y; });
				}

				function dblclick(d) {
				  d3.select(this).classed("fixed", d.fixed = false);
				}

				function dragstart(d) {
				  d3.select(this).classed("fixed", d.fixed = true);
				}*/
				
			});
			
		}
		
	};
}]);