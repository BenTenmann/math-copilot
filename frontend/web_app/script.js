const BACKEND_URL = "http://localhost:9000"

window.addEventListener('DOMContentLoaded', (event) => {
  var canvas = new fabric.Canvas('canvas');
  canvas.isDrawingMode = true;
  canvas.freeDrawingBrush.width = 5;
  canvas.freeDrawingBrush.color = '#000000';

  var markdownPanelWidth = document.getElementById('markdown-panel').offsetWidth;

  function resizeCanvas() {
    canvas.setWidth(window.innerWidth - markdownPanelWidth);
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
    canvas.selection = true; // Enable canvas selection when drawing
    canvas.forEachObject(function(object) {
      object.selectable = true; // Make objects selectable
    });
  });

  var moveButton = document.getElementById('move-button');
  moveButton.addEventListener('click', function() {
    canvas.isDrawingMode = false;
    canvas.selection = false; // Disable canvas selection when moving
    canvas.forEachObject(function(object) {
      object.selectable = false; // Make objects unselectable
    });
  });

  canvas.on('mouse:down', function (options) {
    if (!canvas.isDrawingMode) {
      this.isDragging = true;
      this.selection = false; // Disable canvas selection when dragging
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
    this.selection = true; // Enable canvas selection when mouse is up
  });

  // Convert canvas to image
  function convertToImage() {
    var imageData = canvas.toDataURL("image/png");
    sendToServer(imageData);
  }

  var convertButton = document.getElementById('convert-button');
  convertButton.addEventListener('click', convertToImage);

  // Send image data to server
  function sendToServer(imageData) {
    // Mock server URL
    fetch(`${BACKEND_URL}/latex`, {
      method: 'POST',
      body: JSON.stringify({ image: imageData }),
      headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
      var markdown = data.latex;
      if (!data.is_correct) {
        markdown = `<span style="color:red">${markdown}</span>`
      }
      renderMarkdown(`${markdown}\n>${data.explanation}`);
    })
    .catch(error => console.error('Error:', error));

    // Mock sending image data to server
    console.log("Sending image data to server: ", imageData);
  }

  // Render markdown in the panel
  function renderMarkdown(markdown) {
    var converter = new showdown.Converter(),
    html = converter.makeHtml(markdown);

    var markdownPanel = document.getElementById('markdown-panel');
    markdownPanel.innerHTML = html;

    // Typeset the new content with MathJax
    MathJax.typesetPromise([markdownPanel]);
  }
});
