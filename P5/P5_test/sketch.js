let blocksize = 8;
let Blocks = [];
let blockcount;
let canvas;
let cwidth;
let cheight;

function setup() {
  cwidth = round(windowWidth - 15);
  cheight = round(windowHeight - 15);
  canvas = createCanvas(cwidth,cheight);


  blockcount = 4*2*cwidth / blocksize;
  for (let i = 0; i < blockcount; i++) {
    Blocks.push(new Block((1/4)*i*blocksize,blocksize,blocksize));
    Blocks.push(new Block((1/4)*i*blocksize,blocksize,blocksize));
  }
}

function draw() {
  colorMode(RGB);
  background(25,30);
  colorMode(HSB);

  for (let i = 0; i < blockcount; i++) {
    Blocks[i].move();
    Blocks[i].show();
  }
}

class Block {
  constructor(xpos,rheight,rwidth,yoffset) {
    this.xpos = xpos;
    this.rheight = rheight;
    this.rwidth = rwidth;
    this.ypos = (-2) * rheight;
    this.speed = random(5,20);
    this.hu = random(0,255);
    this.hu_rate = 10;
  }

  show() {
    // fill(100);
    fill(this.hu,255,255)
    // rect(this.xpos,this.ypos,this.rwidth,this.rheight);
    ellipse(this.xpos,this.ypos,this.rwidth,this.rheight);
    this.hu += this.speed / this.hu_rate;
    if (this.hu > 255) {
      this.hu = 0;
    }
  }

  move() {
    this.ypos += this.speed;
    if (this.ypos > cheight) {
      this.ypos = 2 * -cheight;
    }
  }
}