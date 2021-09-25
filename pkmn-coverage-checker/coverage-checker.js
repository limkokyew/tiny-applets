// -----
// Globals and such
// -----

// TODO: Can this be implemented any better?
// Type chart from a defending perspective
const typeChart = {
  "Normal": {
    "Ghost": 0.5,
    "Fighting": 2,
  },
  "Fighting": {
    "Rock": 0.5, "Bug": 0.5, "Dark": 0.5,
    "Flying": 2, "Psychic": 2, "Fairy": 2,
  },
  "Flying": {
    "Fighting": 0.5, "Ground": 0.5, "Bug": 0.5, "Grass": 0.5,
    "Rock": 2, "Electric": 2, "Ice": 2,
  },
  "Poison": {
    "Fighting": 0.5, "Poison": 0.5, "Bug": 0.5, "Grass": 0.5, "Fairy": 0.5,
    "Ground": 2, "Psychic": 2,
  },
  "Ground": {
    "Poison": 0.5, "Rock": 0.5, "Electric": 0.5,
    "Water": 2, "Grass": 2, "Ice": 2,
  },
  "Rock": {
    "Normal": 0.5, "Flying": 0.5, "Poison": 0.5, "Fire": 0.5,
    "Fighting": 2, "Ground": 2, "Steel": 2, "Water": 2, "Grass": 2,
  },
  "Bug": {
    "Fighting": 0.5, "Ground": 0.5, "Grass": 0.5,
    "Flying": 2, "Rock": 2, "Fire": 2,
  },
  "Ghost": {
    "Normal": 0.5, "Fighting": 0.5, "Poison": 0.5, "Bug": 0.5,
    "Ghost": 2, "Dark": 2,
  },
  "Steel": {
    "Normal": 0.5, "Flying": 0.5, "Poison": 0.5, "Rock": 0.5, "Bug": 0.5,
    "Steel": 0.5, "Grass": 0.5, "Psychic": 0.5, "Ice": 0.5, "Dragon": 0.5,
    "Fairy": 0.5,
    "Fighting": 2, "Ground": 2, "Fire": 2,
  },
  "Fire": {
    "Bug": 0.5, "Steel": 0.5, "Fire": 0.5, "Grass": 0.5, "Ice": 0.5,
    "Fairy": 0.5,
    "Ground": 2, "Rock": 2, "Water": 2,
  },
  "Water": {
    "Steel": 0.5, "Fire": 0.5, "Water": 0.5, "Ice": 0.5,
    "Grass": 2, "Electric": 2,
  },
  "Grass": {
    "Ground": 0.5, "Water": 0.5, "Grass": 0.5, "Electric": 0.5,
    "Flying": 2, "Poison": 2, "Bug": 2, "Fire": 2, "Ice": 2,
  },
  "Electric": {
    "Flying": 0.5, "Steel": 0.5, "Electric": 0.5,
    "Ground": 2,
  },
  "Psychic": {
    "Fighting": 0.5, "Psychic": 0.5,
    "Bug": 2, "Ghost": 2, "Dark": 2,
  },
  "Ice": {
    "Ice": 0.5,
    "Fighting": 2, "Rock": 2, "Steel": 2, "Fire": 2,
  },
  "Dragon": {
    "Fire": 0.5, "Water": 0.5, "Grass": 0.5, "Electric": 0.5,
    "Ice": 2, "Dragon": 2, "Fairy": 2,
  },
  "Dark": {
    "Ghost": 0.5, "Psychic": 0.5, "Dark": 0.5,
    "Fighting": 2, "Bug": 2, "Fairy": 2,
  },
  "Fairy": {
    "Fighting": 0.5, "Bug": 0.5, "Dragon": 0.5, "Dark": 0.5,
    "Poison": 2, "Steel": 2,
  }
}

const typeClassname = "type-draggable";
const typeArea = document.getElementById("type-selection-box");
const typeRect = typeArea.getBoundingClientRect();

const dropAreaHighlightClassName = "type-highlighted";
const dropArea = document.getElementById("type-selected");
const dropContainer = document.getElementById("type-selected-container");
const dropRect = dropArea.getBoundingClientRect();

const draggedClassname = "dragged";
const draggedCSSClassName = "type-dragged";

const resultContainerMap = {
  0: document.getElementById("results-effective"),    // Placeholder
  0.5: document.getElementById("results-not-effective"),
  1: document.getElementById("results-effective"),
  2: document.getElementById("results-super-effective")
};

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

function updateResults() {
  const selectedTypes = dropContainer.children;
  const typeMatchups = Object.keys(typeChart).reduce((prev, curr) => (prev[curr] = 0, prev), {});
  const defendingTypes = Array.from(document.getElementsByClassName("type-result"));
  
  // Loop through all types and check how well the user's selected types
  // stack up
  for (const defendingType of defendingTypes) {
    const type = defendingType.attributes.poketype.value;
    let multiplier = 0;
    console.log(type);
    
    for (const selectedType of selectedTypes) {
      const selectedTypeName = selectedType.attributes.poketype.value;
      let currentMultiplier = 0;
      
      // Get the multiplier from the type chart - if it does not
      // exist, assume multiplier to be 1
      if (typeChart[type].hasOwnProperty(selectedTypeName)) {
        currentMultiplier = typeChart[type][selectedTypeName];
      } else {
        currentMultiplier = 1;
      }
      
      // Replace old multiplier if the new one is greater
      if (multiplier < currentMultiplier) {
        multiplier = currentMultiplier;
      }
    }
    
    // Move to the appropriate div
    defendingType.parentElement.removeChild(defendingType);
    resultContainerMap[multiplier].appendChild(defendingType);
    typeMatchups[type] = multiplier;
  }
  
  // console.log(typeMatchups);
}

function addListeners() {
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
    updateResults();
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
