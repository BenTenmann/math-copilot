let canvas1 = document.getElementById("canvas1");
let ctx1 = canvas1.getContext("2d");
ctx1.fillStyle = "lightgreen";
ctx1.fillRect(0, 0, canvas1.width, canvas1.height);

let canvas2 = document.getElementById("canvas2");
let ctx2 = canvas2.getContext("2d");
ctx2.fillStyle = "orange";
ctx2.fillRect(0, 0, canvas2.width, canvas2.height);

// print relative coordinates of mouse on canvas1
canvas1.addEventListener("mousemove", function (e) {
    let x = e.clientX - canvas1.offsetLeft;
    let y = e.clientY - canvas1.offsetTop;
    
    // clear canvas1 and write on it
    ctx1.clearRect(0, 0, canvas1.width, canvas1.height);
    ctx1.fillStyle = "lightgreen";
    ctx1.fillRect(0, 0, canvas1.width, canvas1.height);
    ctx1.fillStyle = "black";
    ctx1.font = "20px Arial";
    ctx1.fillText(x + ", " + y, 10, 25);
});

// print relative coordinates of mouse on canvas2
canvas2.addEventListener("mousemove", function (e) {
    let x = e.clientX - canvas2.offsetLeft;
    let y = e.clientY - canvas2.offsetTop;

    // clear canvas2 and write on it
    ctx2.clearRect(0, 0, canvas2.width, canvas2.height);
    ctx2.fillStyle = "orange";
    ctx2.fillRect(0, 0, canvas2.width, canvas2.height);
    ctx2.fillStyle = "black";
    ctx2.font = "20px Arial";
    ctx2.fillText(x + ", " + y, 10, 25);
});

