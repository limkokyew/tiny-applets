// TODO: Can this be implemented any better?
// Ideally, this would be on another file, but because of CORS, this
// workaround is needed
const typeChart = {
  "Normal": {
    0.5: ["Ghost", "Rock", "Steel"],
    2: []
  },
  "Fighting": {
    0.5: ["Ghost", "Flying", "Poison", "Bug", "Psychic", "Fairy"],
    2: ["Normal", "Rock", "Steel", "Ice", "Dark"]
  },
  "Flying": {
    0.5: ["Rock", "Steel", "Electric"],
    2: ["Fighting", "Bug", "Grass"]
  },
  "Poison": {
    0.5: ["Steel", "Poison", "Ground", "Rock", "Ghost"],
    2: ["Grass", "Fairy"]
  },
  "Ground": {
    0.5: ["Flying", "Bug", "Grass"],
    2: ["Poison", "Rock", "Steel", "Fire", "Electric"]
  },
  "Rock": {
    0.5: ["Fighting", "Ground", "Steel"],
    2: ["Flying", "Bug", "Fire", "Ice"]
  },
  "Bug": {
    0.5: ["Fighting", "Flying", "Poison", "Ghost", "Steel", "Fire", "Fairy"],
    2: ["Grass", "Psychic", "Dark"]
  },
  "Ghost": {
    0.5: ["Normal", "Dark"],
    2: ["Psychic", "Ghost"]
  },
  "Steel": {
    0.5: ["Steel", "Fire", "Water", "Electric"],
    2: ["Rock", "Ice", "Fairy"]
  },
  "Fire": {
    0.5: ["Rock", "Fire", "Water", "Dragon"],
    2: ["Bug", "Steel", "Grass", "Ice"]
  },
  "Water": {
    0.5: ["Water", "Grass", "Dragon"],
    2: ["Ground", "Rock", "Fire"]
  },
  "Grass": {
    0.5: ["Flying", "Poison", "Bug", "Steel", "Fire", "Grass", "Dragon"],
    2: ["Ground", "Rock", "Water"]
  },
  "Electric": {
    0.5: ["Ground", "Grass", "Electric", "Dragon"],
    2: ["Flying", "Water"]
  },
  "Psychic": {
    0.5: ["Dark", "Steel", "Psychic"],
    2: ["Fighting", "Poison"]
  },
  "Ice": {
    0.5: ["Steel", "Fire", "Water", "Ice"],
    2: ["Flying", "Ground", "Grass", "Dragon"]
  },
  "Dragon": {
    0.5: ["Fairy", "Steel"],
    2: ["Dragon"]
  },
  "Dark": {
    0.5: ["Fighting", "Dark", "Fairy"],
    2: ["Ghost", "Psychic"]
  },
  "Fairy": {
    0.5: ["Poison", "Fire", "Steel"],
    2: ["Fighting", "Dragon", "Dark"]
  }
}

// -----
// Globals and such
// -----
const typeClassname = "type-draggable";
const typeArea = document.getElementById("type-selection-box");
const typeRect = typeArea.getBoundingClientRect();

const dropAreaHighlightClassName = "type-highlighted";
const dropArea = document.getElementById("type-selected");
const dropContainer = document.getElementById("type-selected-container");
const dropRect = dropArea.getBoundingClientRect();

const draggedClassname = "dragged";
const draggedCSSClassName = "type-dragged";

const isInTypeRect = (x, y) => {
  return (x >= typeRect.left && x <= typeRect.right
       && y >= typeRect.top && y <= typeRect.bottom);
};
const isInDropRect = (x, y) => {
  return (x >= dropRect.left && x <= dropRect.right
       && y >= dropRect.top && y <= dropRect.bottom);
};

let xOffset = 0;
let yOffset = 0;

// -----
// Main functions
// -----

function addListeners(){
  let types = document.getElementsByClassName(typeClassname);
  for (let i = 0; i < types.length; i++) {
    types[i].addEventListener("mousedown", mouseDown, false);
  }
  window.addEventListener("mouseup", mouseUp, false);
}

function mouseUp(e) {
  window.removeEventListener("mousemove", divMove, true);
  let divs = document.getElementsByClassName(draggedClassname);
  if (divs.length > 0) {
    dropArea.classList.remove(dropAreaHighlightClassName);
    let target = divs[0];
    target.classList.remove(draggedClassname, draggedCSSClassName);
    target.style.position = "";
    target.style.top = "";
    target.style.left = "";
    
    const inTypeRect = isInTypeRect(e.clientX, e.clientY);
    const inDropRect = isInDropRect(e.clientX, e.clientY);
    
    if (inDropRect) {
      typeArea.removeChild(target);
      dropContainer.appendChild(target);
    } else {
      dropContainer.removeChild(target);
      typeArea.appendChild(target);
    }
  }
}

function mouseDown(e) {
  e.target.classList.add(draggedClassname, draggedCSSClassName);
  let boundingRect = e.target.getBoundingClientRect();
  xOffset = e.clientX - boundingRect.left;
  yOffset = e.clientY - boundingRect.top;
  window.addEventListener("mousemove", divMove, true);
}

function divMove(e) {
  let div = document.getElementsByClassName(draggedClassname)[0];
  div.style.position = "absolute";
  div.style.top = (e.clientY - yOffset) + "px";
  div.style.left = (e.clientX - xOffset) + "px";
  
  if (isInDropRect(e.clientX, e.clientY)) {
    dropArea.classList.add(dropAreaHighlightClassName);
  } else {
    dropArea.classList.remove(dropAreaHighlightClassName);
  }
}

function setTypeOrder() {
  let types = document.getElementsByClassName("type");
  for (let i = 0; i < types.length; i++) {
    types[i].style.order = i;
  }
}

window.onload = addListeners;
setTypeOrder();
