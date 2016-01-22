angular.module("annotate-canvas-directive", [])

.directive("annotateCanvas", [function() {
	return {
		restrict: "E",
        replace: true,
        templateUrl: "templates/annotate-canvas.html",
		link: function(scope, element, attrs) {
            
            var context = element[0].getContext("2d");
            
            // add image
            var imageObj = new Image();
            
            imageObj.onload = function() {
                context.drawImage(imageObj, 0, 0, 700, 1000);
            };
            
            imageObj.src = "a01-030.png";
            
            var tool = new tool_pencil();
            
            // bind events
            element.on("mousemove", ev_canvas);
            element.on("mousedown", ev_canvas);
            element.on("mouseup", ev_canvas);
                       
           var started = false;
            function ev_mousemove (ev) {
                var x, y;

                // Get the mouse position relative to the <canvas> element
                if (ev.layerX || ev.layerX == 0) { // Firefox
                    x = ev.layerX;
                    y = ev.layerY;
                } else if (ev.offsetX || ev.offsetX == 0) { // Opera
                    x = ev.offsetX;
                    y = ev.offsetY;
                }

                // The event handler works like a drawing pencil which
                // tracks the mouse movements. We start drawing a path made up of lines
                if (!started) {
                    context.beginPath();
                    context.moveTo(x, y);
                    started = true;
                } else {
                    context.lineTo(x, y);
                    context.stroke();
                }
            };
            
            // This painting tool works like a drawing
            // pencil which tracks the mouse movements
            function tool_pencil () {
                var tool = this;
                this.started = false;

                // This is called when you start holding down the mouse button
                // This starts the pencil drawing
                this.mousedown = function (ev) {
                        context.beginPath();
                        context.moveTo(ev._x, ev._y);
                        tool.started = true;
                };

                // This function is called every time you move the mouse. Obviously, it only
                // draws if the tool.started state is set to true (when you are holding down
                // the mouse button)
                this.mousemove = function (ev) {
                    if (tool.started) {
                        context.lineTo(ev._x, ev._y);
                        context.stroke();
                    }
                };

                // This is called when you release the mouse button
                this.mouseup = function (ev) {
                    if (tool.started) {
                        tool.mousemove(ev);
                        tool.started = false;
                    }
                };
            }

            // The general-purpose event handler. This function just determines
            // the mouse position relative to the <canvas> element
            function ev_canvas (ev) {
                // Firefox
                if (ev.layerX || ev.layerX == 0) {
                    ev._x = ev.layerX;
                    ev._y = ev.layerY;
                // Opera
                } else if (ev.offsetX || ev.offsetX == 0) {
                    ev._x = ev.offsetX;
                    ev._y = ev.offsetY;
                }

                // Call the event handler of the tool
                var func = tool[ev.type];
                if (func) {
                    func(ev);
                }
            }
                                           
            // bind data
            /*
            
            
              var canvas, context, canvaso, contexto;

  // The active tool instance.
  var tool;
  var tool_default = 'rect';

  function init () {
    // Find the canvas element.
    canvaso = document.getElementById('imageView');
    if (!canvaso) {
      alert('Error: I cannot find the canvas element!');
      return;
    }

    if (!canvaso.getContext) {
      alert('Error: no canvas.getContext!');
      return;
    }

    // Get the 2D canvas context.
    contexto = canvaso.getContext('2d');
    if (!contexto) {
      alert('Error: failed to getContext!');
      return;
    }

    // Add the temporary canvas.
    var container = canvaso.parentNode;
    canvas = document.createElement('canvas');
    if (!canvas) {
      alert('Error: I cannot create a new canvas element!');
      return;
    }

    canvas.id     = 'imageTemp';
    canvas.width  = canvaso.width;
    canvas.height = canvaso.height;
    container.appendChild(canvas);

    context = canvas.getContext('2d');

    // Get the tool select input.
    var tool_select = document.getElementById('dtool');
    if (!tool_select) {
      alert('Error: failed to get the dtool element!');
      return;
    }
    tool_select.addEventListener('change', ev_tool_change, false);

    // Activate the default tool.
    if (tools[tool_default]) {
      tool = new tools[tool_default]();
      tool_select.value = tool_default;
    }

    // Attach the mousedown, mousemove and mouseup event listeners.
    canvas.addEventListener('mousedown', ev_canvas, false);
    canvas.addEventListener('mousemove', ev_canvas, false);
    canvas.addEventListener('mouseup',   ev_canvas, false);
  }

  // The general-purpose event handler. This function just determines the mouse 
  // position relative to the canvas element.
  function ev_canvas (ev) {
    if (ev.layerX || ev.layerX == 0) { // Firefox
      ev._x = ev.layerX;
      ev._y = ev.layerY;
    } else if (ev.offsetX || ev.offsetX == 0) { // Opera
      ev._x = ev.offsetX;
      ev._y = ev.offsetY;
    }

    // Call the event handler of the tool.
    var func = tool[ev.type];
    if (func) {
      func(ev);
    }
  }

  // The event handler for any changes made to the tool selector.
  function ev_tool_change (ev) {
    if (tools[this.value]) {
      tool = new tools[this.value]();
    }
  }

  // This function draws the #imageTemp canvas on top of #imageView, after which 
  // #imageTemp is cleared. This function is called each time when the user 
  // completes a drawing operation.
  function img_update () {
		contexto.drawImage(canvas, 0, 0);
		context.clearRect(0, 0, canvas.width, canvas.height);
  }

  // This object holds the implementation of each drawing tool.
  var tools = {};

  // The drawing pencil.
  tools.pencil = function () {
    var tool = this;
    this.started = false;

    // This is called when you start holding down the mouse button.
    // This starts the pencil drawing.
    this.mousedown = function (ev) {
        context.beginPath();
        context.moveTo(ev._x, ev._y);
        tool.started = true;
    };

    // This function is called every time you move the mouse. Obviously, it only 
    // draws if the tool.started state is set to true (when you are holding down 
    // the mouse button).
    this.mousemove = function (ev) {
      if (tool.started) {
        context.lineTo(ev._x, ev._y);
        context.stroke();
      }
    };

    // This is called when you release the mouse button.
    this.mouseup = function (ev) {
      if (tool.started) {
        tool.mousemove(ev);
        tool.started = false;
        img_update();
      }
    };
  };

  // The rectangle tool.
  tools.rect = function () {
    var tool = this;
    this.started = false;

    this.mousedown = function (ev) {
      tool.started = true;
      tool.x0 = ev._x;
      tool.y0 = ev._y;
    };

    this.mousemove = function (ev) {
      if (!tool.started) {
        return;
      }

      var x = Math.min(ev._x,  tool.x0),
          y = Math.min(ev._y,  tool.y0),
          w = Math.abs(ev._x - tool.x0),
          h = Math.abs(ev._y - tool.y0);

      context.clearRect(0, 0, canvas.width, canvas.height);

      if (!w || !h) {
        return;
      }

      context.strokeRect(x, y, w, h);
    };

    this.mouseup = function (ev) {
      if (tool.started) {
        tool.mousemove(ev);
        tool.started = false;
        img_update();
      }
    };
  };

  init();
            
            
            
            
            
            
            
            scope.$watch("geojson", function(newData, oldData) {
                
                // async check
                if (newData !== undefined) {
                    
                    // check new vs old
                    var isMatching = angular.equals(newData, oldData);
                    
                    // if false
                    if (!isMatching) {
                        
                        // update the viz
                        draw(newData);
                        
                    };
                    
                };
                
            });*/
			
		}
		
	};
	
}]);