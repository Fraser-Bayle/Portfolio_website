class MatrixRain {
    constructor() {
        this.canvas = document.createElement('canvas');
        this.canvas.id = 'matrixCanvas';
        this.context = this.canvas.getContext('2d');

        // Style the canvas
        this.canvas.style.position = 'fixed';
        this.canvas.style.top = '0';
        this.canvas.style.left = '0';
        this.canvas.style.width = '100%';
        this.canvas.style.height = '100%';
        this.canvas.style.zIndex = '-1';

        // Add canvas to the page
        document.body.appendChild(this.canvas);

        // Set up characters
        this.katakana = 'アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルグズブヅプエェケセテネヘメレヱゲゼデベペオォコソトノホモヨョロヲゴゾドボポヴッン';
        this.latin = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
        this.nums = '0123456789';
        this.alphabet = this.katakana + this.latin + this.nums;

        this.fontSize = 16;
        this.rainDrops = [];

        // Bind resize handler
        this.resize = this.resize.bind(this);
        window.addEventListener('resize', this.resize);

        // Initial setup
        this.resize();
        this.initializeDrops();
        this.animate();
    }

    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
        this.columns = Math.floor(this.canvas.width/this.fontSize);
        this.initializeDrops();
    }

    initializeDrops() {
        this.rainDrops = [];
        for(let x = 0; x < this.columns; x++) {
            this.rainDrops[x] = 1;
        }
    }

    draw() {
        this.context.fillStyle = 'rgba(0, 0, 0, 0.05)';
        this.context.fillRect(0, 0, this.canvas.width, this.canvas.height);

        this.context.fillStyle = '#0F0';
        this.context.font = this.fontSize + 'px monospace';

        for(let i = 0; i < this.rainDrops.length; i++) {
            const text = this.alphabet.charAt(Math.floor(Math.random() * this.alphabet.length));
            this.context.fillText(text, i*this.fontSize, this.rainDrops[i]*this.fontSize);

            if(this.rainDrops[i]*this.fontSize > this.canvas.height && Math.random() > 0.975) {
                this.rainDrops[i] = 0;
            }
            this.rainDrops[i]++;
        }
    }

    animate() {
        this.draw();
        requestAnimationFrame(() => this.animate());
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    new MatrixRain();
});