window.addEventListener('DOMContentLoaded', (event) => {
    // Initialize the canvas
    var canvas = new fabric.Canvas('canvas');
  
    // Set the brush properties
    canvas.isDrawingMode = true;
    canvas.freeDrawingBrush.width = 5;
    canvas.freeDrawingBrush.color = '#000000';
  
    // Adjust the canvas size to fit the window
    function resizeCanvas() {
      canvas.setWidth(window.innerWidth);
      canvas.setHeight(window.innerHeight);
      canvas.renderAll();
    }
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
  
    // Save the canvas as an image
    function saveCanvas() {
      canvas.isDrawingMode = false;
      var dataURL = canvas.toDataURL({ format: 'png' });
      var link = document.createElement('a');
      link.href = dataURL;
      link.download = 'canvas_image.png';
      link.click();
      canvas.isDrawingMode = true;
    }
  
    // Undo the last drawing action
    function undo() {
      var objects = canvas.getObjects();
      if (objects.length > 0) {
        canvas.remove(objects[objects.length - 1]);
        canvas.renderAll();
      }
    }
  
    // Event listener for the Undo button
    var undoButton = document.getElementById('undo-button');
    undoButton.addEventListener('click', undo);
  
    // Add the ability to move the view of the canvas
    canvas.on('mouse:down', function (options) {
      var evt = options.e;
      if (evt.altKey === true) {
        this.isDragging = true;
        this.selection = false;
        this.lastPosX = evt.clientX;
        this.lastPosY = evt.clientY;
      }
    });
  
    canvas.on('mouse:move', function (options) {
      if (this.isDragging) {
        var e = options.e;
        var vpt = this.viewportTransform;
        vpt[4] += e.clientX - this.lastPosX;
        vpt[5] += e.clientY - this.lastPosY;
        this.requestRenderAll();
        this.lastPosX = e.clientX;
        this.lastPosY = e.clientY;
      }
    });
  
    canvas.on('mouse:up', function (options) {
      this.isDragging = false;
      this.selection = true;
    });
});