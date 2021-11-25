// Document elements
const blockerElement = document.getElementById("blocker");
const boardContainer = document.getElementById("board-container");
const flipLevel = document.getElementById("flip-level");
const flipCurrentScore = document.getElementById("flip-current-score");
const flipTotalScore = document.getElementById("flip-total-score");

// Game data
let tileElements = [];
let level = 1;
let totalScore = 0;
let score = 1;
let revealedTiles = 0;

// Taken from MDN ()
function getRandomInt(max) {
  return Math.floor(Math.random() * max);
}

function getRandomTileElement() {
  let tileElement = getRandomInt(4) + 1;
  if (tileElement === 4) {
    tileElement = "💣";
  }
  
  return tileElement;
}

function gameOver() {
  blocker.classList.add("show");
  
}

/** 
 * Updates current score with the total multiplier and adjusts the total score
 * accordingly.
 * 
 * @param {number} multiplier Integer to multiply the current score with.
 */
function updateScore(multiplier) {
  score *= multiplier;
  flipCurrentScore.innerHTML = score;
  flipTotalScore.innerHTML = totalScore + score;
}

function TileContainer(props) {
  return React.createElement(
    "div",
    {id: "tile-container", className: "flex"},
    props.items
  );
}

function Tile(props) {
  const content = props.content;
  const [revealed, setRevealed] = React.useState(false);
  const revealFunc = () => {
    if (!revealed) {
      setRevealed(true);
      revealedTiles++;
      
      if (content !== "💣") {
        updateScore(content);
        if (revealedTiles === 25) {
          lv++;
          console.log("Advance game!");
        }
      } else {
        gameOver();
      }
    };
  }
  
  return React.createElement(
    "button",
    {className: `tile ${revealed ? "revealed" : ""}`, onClick: revealFunc},
    `${revealed ? content : ""}`
  );
}

function initializeLevel(lvl) {
  flipLevel.innerHTML = `Lv. ${lvl}`;
  for (let i = 0; i < 25; i++) {
    tileElements.push(
        React.createElement(Tile, {"content": getRandomTileElement(), "key": i})
    );
  }
  
  const tc = React.createElement(TileContainer, {"items": tileElements});
  ReactDOM.render(tc, boardContainer);
  
  console.log(tileElements);
}

initializeLevel(level);
