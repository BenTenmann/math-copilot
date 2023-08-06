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
