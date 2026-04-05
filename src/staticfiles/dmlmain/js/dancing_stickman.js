"use strict";
class StickmanDancer {
    canvas;
    ctx;
    isAnimating = false;
    frame = 0;
    constructor() {
        this.canvas = document.createElement('canvas');
        this.canvas.width = 400;
        this.canvas.height = 500;
        this.canvas.style.border = '1px solid black';
        this.canvas.style.cursor = 'pointer';
        document.body.appendChild(this.canvas);
        this.ctx = this.canvas.getContext('2d');
        this.canvas.addEventListener('click', () => this.startDance());
    }
    drawStickman(offsetY) {
        const x = 200;
        const y = 150 + offsetY;
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.ctx.strokeStyle = 'black';
        this.ctx.lineWidth = 2;
        this.ctx.beginPath();
        this.ctx.arc(x, y - 50, 20, 0, Math.PI * 2);
        this.ctx.stroke();
        this.ctx.beginPath();
        this.ctx.moveTo(x, y - 30);
        this.ctx.lineTo(x, y + 40);
        this.ctx.stroke();
        this.ctx.beginPath();
        this.ctx.moveTo(x, y - 10);
        this.ctx.lineTo(x - 50, y - 40 + Math.sin(this.frame * 0.1) * 30);
        this.ctx.stroke();
        this.ctx.beginPath();
        this.ctx.moveTo(x, y - 10);
        this.ctx.lineTo(x + 50, y - 40 - Math.sin(this.frame * 0.1) * 30);
        this.ctx.stroke();
        this.ctx.beginPath();
        this.ctx.moveTo(x, y + 40);
        this.ctx.lineTo(x - 30, y + 90 + Math.sin(this.frame * 0.12) * 20);
        this.ctx.stroke();
        this.ctx.beginPath();
        this.ctx.moveTo(x, y + 40);
        this.ctx.lineTo(x + 30, y + 90 - Math.sin(this.frame * 0.12) * 20);
        this.ctx.stroke();
    }
    startDance() {
        if (this.isAnimating)
            return;
        this.isAnimating = true;
        this.frame = 0;
        const animate = () => {
            this.drawStickman(Math.sin(this.frame * 0.05) * 10);
            this.frame++;
            if (this.frame < 120) {
                requestAnimationFrame(animate);
            }
            else {
                this.isAnimating = false;
                this.drawStickman(0);
            }
        };
        animate();
    }
}
function main() {
    console.log("Hello, DMLStar!");
}
main();
new StickmanDancer();
