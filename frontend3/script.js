window.addEventListener('DOMContentLoaded', (event) => {
  var canvas = new fabric.Canvas('canvas');
  canvas.isDrawingMode = true;
  canvas.freeDrawingBrush.width = 5;
  canvas.freeDrawingBrush.color = '#000000';

  function resizeCanvas() {
    canvas.setWidth(window.innerWidth);
    canvas.setHeight(window.innerHeight);
    canvas.renderAll();
  }
  resizeCanvas();
  window.addEventListener('resize', resizeCanvas);

  function undo() {
    var objects = canvas.getObjects();
    if (objects.length > 0) {
      canvas.remove(objects[objects.length - 1]);
      canvas.renderAll();
    }
  }

  var undoButton = document.getElementById('undo-button');
  undoButton.addEventListener('click', undo);

  var drawButton = document.getElementById('draw-button');
  drawButton.addEventListener('click', function() {
    canvas.isDrawingMode = true;
  });

  var moveButton = document.getElementById('move-button');
  moveButton.addEventListener('click', function() {
    canvas.isDrawingMode = false;
  });

  canvas.on('mouse:down', function (options) {
    if (!canvas.isDrawingMode) {
      this.isDragging = true;
      this.selection = false;
      this.lastPosX = options.e.clientX;
      this.lastPosY = options.e.clientY;
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