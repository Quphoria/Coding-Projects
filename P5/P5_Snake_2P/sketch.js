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
let C1_Snake;
let C2_Snake;
let highscore = 0;
let game = {
  p1over:true,
  p2over:true,
  pause:false,
  singleplayer:true
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

function p1newGame() {
  game.p1over = false;
  if (game.p2over) {
    game.pause = false;
  } else if (game.singleplayer) {
    document.getElementById("LenSpan").style.display = "none";
    document.getElementById("2PLenSpan").style.display = "";
    game.singleplayer = false;
  }
  C_Food = new Food(
    0.5*blocksize+blocksize * floor(
      random(0,x_blockcount)),
    0.5*blocksize+blocksize * floor(
      random(0,y_blockcount)),
    blocksize,25,200,50);
  C1_Snake = new Snake(200,100,0,0,150,200,1,1);
}

function p2newGame() {
  game.p2over = false;
  if (game.p1over) {
    game.pause = false;
  } else if (game.singleplayer) {
    document.getElementById("LenSpan").style.display = "none";
    document.getElementById("2PLenSpan").style.display = "";
    game.singleplayer = false;
  }
  C_Food = new Food(
    0.5*blocksize+blocksize * floor(
      random(0,x_blockcount)),
    0.5*blocksize+blocksize * floor(
      random(0,y_blockcount)),
    blocksize,25,200,50);
  C2_Snake = new Snake(255,0,100,125,0,255,1,2);
}

function keyPressed() {
  if (keyCode === UP_ARROW) {
    if (game.p1over) {
      p1newGame();
    }
    if (!game.pause && (C1_Snake.length == 1 ||
        C1_Snake.currentDirection != 3)) {
      C1_Snake.direction = 1;
    }
  } else if (keyCode === DOWN_ARROW) {
    if (game.p1over) {
      p1newGame();
    }
    if (!game.pause && (C1_Snake.length == 1 ||
        C1_Snake.currentDirection != 1)) {
      C1_Snake.direction = 3;
    }
  } else if (keyCode === RIGHT_ARROW) {
    if (game.p1over) {
      p1newGame();
    }
    if (!game.pause && (C1_Snake.length == 1 ||
        C1_Snake.currentDirection != 4)) {
      C1_Snake.direction = 2;
    }
  } else if (keyCode === LEFT_ARROW) {
    if (game.p1over) {
      p1newGame();
    }
    if (!game.pause && (C1_Snake.length == 1 ||
        C1_Snake.currentDirection != 2)) {
      C1_Snake.direction = 4;
    }
  } else if (key == "W") {
    if (game.p2over) {
      p2newGame();
    }
    if (!game.pause && (C2_Snake.length == 1 ||
        C2_Snake.currentDirection != 3)) {
      C2_Snake.direction = 1;
    }
  } else if (key == "S") {
    if (game.p2over) {
      p2newGame();
    }
    if (!game.pause && (C2_Snake.length == 1 ||
        C2_Snake.currentDirection != 1)) {
      C2_Snake.direction = 3;
    }
  } else if (key == "D") {
    if (game.p2over) {
      p2newGame();
    }
    if (!game.pause && (C2_Snake.length == 1 ||
        C2_Snake.currentDirection != 4)) {
      C2_Snake.direction = 2;
    }
  } else if (key == "A") {
    if (game.p2over) {
      p2newGame();
    }
    if (!game.pause && (C2_Snake.length == 1 ||
        C2_Snake.currentDirection != 2)) {
      C2_Snake.direction = 4;
    }
  } else if (key == " ") {
    if (!game.p1over || !game.p2over) {
      game.pause = !game.pause;
    }
  }
  return false; // prevent default
}

function displayLengths() {
  if (game.singleplayer) {
    p1elementname = "Length";
    p2elementname = "Length";
  } else {
    p1elementname = "P1Length";
    p2elementname = "P2Length";
  }
  if (!game.p1over) {
    document.getElementById(p1elementname).innerHTML = C1_Snake.length;
    highscore = max(C1_Snake.length,highscore);
  }
  if (!game.p2over) {
    document.getElementById(p2elementname).innerHTML = C2_Snake.length;
    highscore = max(C2_Snake.length,highscore);
  }
  document.getElementById("Highscore").innerHTML = highscore;
}

function draw() {
  displayLengths();
  p1over = game.p1over;
  p2over = game.p2over;
  if ((!p1over) || (!p2over)) {
    background(25,225);
    l1 = 0;
    l2 = 0;
    if (!p1over) {
      l1 = C1_Snake.length
    }
    if (!p2over) {
      l2 = C2_Snake.length
    }
    frameRate(min(60,max(10,10+max(l1,l2))));
    if (!game.pause) {
      if (!p1over && !p2over) {
        C1_Snake.move();
        C2_Snake.move();
        C1_Snake.collision(C2_Snake.history)
        C2_Snake.collision(C1_Snake.history)
        C1_Snake.collect(C_Food);
        C2_Snake.collect(C_Food);
      }
      else if (!p1over) {
        C1_Snake.move();
        C1_Snake.collision([])
        C1_Snake.collect(C_Food);
      }
      else if (!p2over) {
        C2_Snake.move();
        C2_Snake.collision([])
        C2_Snake.collect(C_Food);
      }
    }

    while (C_Food.collected) {
      C_Food = new Food(
        0.5*blocksize+blocksize * floor(
          random(0,x_blockcount)),
        0.5*blocksize+blocksize * floor(
          random(0,y_blockcount)),
        blocksize,25,200,50);
      if (!p1over) {
        C1_Snake.collect(C_Food);
      }
      if (!p2over) {
        C2_Snake.collect(C_Food);
      }
    }
    C_Food.show();
    if (!p1over) {
      C1_Snake.show();
    }
    if (!p2over) {
      C2_Snake.show();
    }
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
  constructor(hr,hg,hb,r,g,b,length,snakenumber) {
    this.r = r;
    this.g = g;
    this.b = b;
    this.length = length;
    this.snakenumber = snakenumber;
    this.history = [];
    if (game.singleplayer) {
      this.history.push(new Body(
        blocksize*floor(x_blockcount*0.5),
        blocksize*floor(y_blockcount*0.5),
        // blocksize,this.r,this.g,this.b));
        blocksize,hr,hg,hb));
    } else {
      this.history.push(new Body(
        blocksize+blocksize * floor(random(0,x_blockcount)),
        blocksize+blocksize * floor(random(0,y_blockcount)),
        // blocksize,this.r,this.g,this.b));
        blocksize,hr,hg,hb));
    }
    this.direction = 0;
    this.currentDirection  = 0;
  }

  show() {
    for (let i = 0; i < this.history.length; i++) {
      this.history[i].show();
    }
    if (this.snakenumber == 1 && game.p1over) {
      this.history[0].r = 0;
      this.history[0].g = 50;
      this.history[0].b = 255;
      this.history[0].show();
    } else if (this.snakenumber == 2 && game.p2over) {
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

    }
  }

  collision(other_snake) {
    for (let i = 0; i < this.history.length; i++) {
      if (i != 0) {
        if (this.history[0].xpos == this.history[i].xpos &&
          this.history[0].ypos == this.history[i].ypos) {
          if (this.snakenumber == 1) {
            game.p1over = true;
          } else if (this.snakenumber == 2) {
            game.p2over = true;
          }
        }
      }
    }
    for (let i = 0; i < other_snake.length; i++) {
      if (this.history[0].xpos == other_snake[i].xpos &&
        this.history[0].ypos == other_snake[i].ypos) {
        if (this.snakenumber == 1) {
          game.p1over = true;
        } else if (this.snakenumber == 2) {
          game.p2over = true;
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