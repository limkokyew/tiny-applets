const tileElements = [];
const boardContainer = document.getElementById("board-container");

function TileContainer(props) {
  return React.createElement(
    "div",
    {id: "tile-container", className: "flex"},
    props.items
  );
}

function Tile(props) {
  const content = props.content;
  let revealed = false;
  
  return React.createElement(
    "div",
    {className: "tile"},
    content
  );
}

function initializeGame() {
  for (let i = 0; i < 9; i++) {
    tileElements.push(React.createElement(Tile, {"content": "Test", "key": i}));
  }
  
  const tc = React.createElement(TileContainer, {"items": tileElements});
  ReactDOM.render(tc, boardContainer);
  
  console.log(tileElements);
}

initializeGame();
