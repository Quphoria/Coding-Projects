const minBlockCount = 10;
const maxBlockCount = 80;
const mult_blocksize = 5;
const minBlockSize = 15;

let blocksize;
let cwidth;
let cheight;
let x_blockcount;
let y_blockcount;

let C_Food;
let C_Snake;
let highscore = 0;
let game = {
  over:true,
  pause:false
};

function CalculateSize(win_width,win_height) {
  calculatedSize = false;
  blocksize = mult_blocksize;
  let largestBlocksize;
  let last_blocksize = blocksize;
  let gotMax = false;
  let gotMin = false;

  while (!calculatedSize) {
    console.log(blocksize)
    cwidth = floor((win_width - blocksize)/blocksize)*blocksize;
    cheight = floor((win_height - blocksize)/blocksize)*blocksize;
    x_blockcount = floor(cwidth / blocksize);
    y_blockcount = floor(cheight / blocksize);
    if (!gotMax) {
      if (x_blockcount > maxBlockCount || y_blockcount > minBlockCount) {
        blocksize += mult_blocksize;
      } else {
        last_blocksize = blocksize;
        largestBlocksize = blocksize;
        gotMax = true;
        // calculatedSize = true;
      }
    } else {
      if ((x_blockcount > maxBlockCount || y_blockcount > maxBlockCount) || blocksize == mult_blocksize) {
        calculatedSize = true;
        last_blocksize = blocksize;
      } else {
        blocksize -= mult_blocksize;
        blocksize = min(largestBlocksize,max(mult_blocksize,blocksize));
      }
    }
  }

  blocksize = max(last_blocksize,minBlockSize);
  cwidth = floor((win_width - blocksize)/blocksize)*blocksize;
  cheight = floor((win_height - blocksize)/blocksize)*blocksize;
  x_blockcount = floor(cwidth / blocksize);
  y_blockcount = floor(cheight / blocksize);
}

function setup() {
  CalculateSize(windowWidth,windowHeight-20);

  createCanvas(cwidth,cheight);

  background(25);
  noStroke();
}

function newGame() {
  game.over = false;
  game.pause = false;
  C_Food = new Food(
    0.5*blocksize+blocksize * floor(
      random(0,x_blockcount)),
    0.5*blocksize+blocksize * floor(
      random(0,y_blockcount)),
    blocksize,25,200,50);
  C_Snake = new Snake(200,100,0,0,150,200,1);
}

function keyPressed() {
  if (keyCode === UP_ARROW) {
    if (game.over) {
      newGame();
    }
    if (!game.pause && (C_Snake.length == 1 ||
        C_Snake.currentDirection != 3)) {
      C_Snake.direction = 1;
    }
  } else if (keyCode === DOWN_ARROW) {
    if (game.over) {
      newGame();
    }
    if (!game.pause && (C_Snake.length == 1 ||
        C_Snake.currentDirection != 1)) {
      C_Snake.direction = 3;
    }
  } else if (keyCode === RIGHT_ARROW) {
    if (game.over) {
      newGame();
    }
    if (!game.pause && (C_Snake.length == 1 ||
        C_Snake.currentDirection != 4)) {
      C_Snake.direction = 2;
    }
  } else if (keyCode === LEFT_ARROW) {
    if (game.over) {
      newGame();
    }
    if (!game.pause && (C_Snake.length == 1 ||
        C_Snake.currentDirection != 2)) {
      C_Snake.direction = 4;
    }
  } else if (key == " ") {
    if (!game.over) {
      game.pause = !game.pause;
    }
  }
  return false; // prevent default
}

function draw() {

  if (!game.over) {
    document.getElementById("Length").innerHTML = C_Snake.length;
    highscore = max(C_Snake.length,highscore);
    document.getElementById("Highscore").innerHTML = highscore;
    background(25,225);
    frameRate(min(60,max(10,10+C_Snake.length)));

    if (!game.pause) {
      C_Snake.move();
    }

    C_Snake.collect(C_Food);

    while (C_Food.collected) {
      C_Food = new Food(
        0.5*blocksize+blocksize * floor(
          random(0,x_blockcount)),
        0.5*blocksize+blocksize * floor(
          random(0,y_blockcount)),
        blocksize,25,200,50);
      C_Snake.collect(C_Food);
    }
    C_Food.show();
    C_Snake.show();
  }
}

class Block {
  constructor(xpos,ypos,rwidth,r,g,b,square) {
    this.xpos = xpos;
    this.ypos = ypos;
    this.rwidth = rwidth;
    this.square = square

    this.r = r;
    this.g = g;
    this.b = b;
  }

  show() {
    // fill(100);
    fill(this.r,this.g,this.b);
    // rect(this.xpos,this.ypos,this.rwidth,this.rheight);
    if (this.square) {
      rectMode(CORNER)
      rect(this.xpos,this.ypos,this.rwidth,this.rwidth);
    } else {
      ellipseMode(CENTER)
      ellipse(this.xpos,this.ypos,this.rwidth,this.rwidth);
    }

  }
}

class Food extends Block {
  constructor(xpos,ypos,rwidth,r,g,b) {
    super(xpos,ypos,rwidth,r,g,b,false);
    this.collected = false;
    this.energy = 1;
  }
}

class Body extends Block {
  constructor(xpos,ypos,rwidth,r,g,b) {
    super(xpos,ypos,rwidth,r,g,b,true);
  }
}

class Snake {
  constructor(hr,hg,hb,r,g,b,length) {
    this.r = r;
    this.g = g;
    this.b = b;
    this.length = length;
    this.history = [];
    this.history.push(new Body(
      blocksize*floor(x_blockcount*0.5),
      blocksize*floor(y_blockcount*0.5),
      // blocksize,this.r,this.g,this.b));
      blocksize,hr,hg,hb));
    this.direction = 0;
    this.currentDirection  = 0;
  }

  show() {
    for (let i = 0; i < this.history.length; i++) {
      this.history[i].show();
    }
    if (game.over) {
      this.history[0].r = 0;
      this.history[0].g = 50;
      this.history[0].b = 255;
      this.history[0].show();
    }
  }

  move() {
    this.currentDirection  = this.direction;
    if (this.currentDirection != 0) {
      let prev_x;
      let prev_y;
      let old_prev_x;
      let old_prev_y;

      for (let i = 0; i < this.history.length; i++) {
        old_prev_x = prev_x;
        old_prev_y = prev_y;
        prev_x = this.history[i].xpos;
        prev_y = this.history[i].ypos;
        if (i == 0) {
          switch (this.currentDirection) {
            case 1:
              this.history[i].ypos -= blocksize;
              break;
            case 2:
              this.history[i].xpos += blocksize;
              break;
            case 3:
              this.history[i].ypos += blocksize;
              break;
            case 4:
              this.history[i].xpos -= blocksize;
              break;

          }
          if (this.history[i].xpos < 0) {
            this.history[i].xpos = (x_blockcount-1)*blocksize;
          }
          if (this.history[i].ypos < 0) {
            this.history[i].ypos = (y_blockcount-1)*blocksize;
          }
          if (this.history[i].xpos > (x_blockcount-1)*blocksize) {
            this.history[i].xpos = 0;
          }
          if (this.history[i].ypos > (y_blockcount-1)*blocksize) {
            this.history[i].ypos = 0;
          }
        } else {
          this.history[i].xpos = old_prev_x;
          this.history[i].ypos = old_prev_y;
        }
      }
      if (this.length > this.history.length) {
        this.history.push(new Body(prev_x,prev_y,blocksize,this.r,this.g,this.b));
      }
      for (let i = 0; i < this.history.length; i++) {
        if (i != 0) {
          if (this.history[0].xpos == this.history[i].xpos &&
            this.history[0].ypos == this.history[i].ypos) {
              game.over = true;
            }
        }
      }
    }
  }

  collect(Food_Obj) {
    for (let i = 0; i < this.history.length; i++) {
      if (Food_Obj.xpos == 0.5*blocksize+this.history[i].xpos && Food_Obj.ypos == 0.5*blocksize+this.history[i].ypos) {
          Food_Obj.collected = true;
          this.length += Food_Obj.energy;
      }
    }
  }
}