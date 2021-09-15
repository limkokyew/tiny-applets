// -----
// Globals and such
// -----
const typeClassname = "type";
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
window.onload = addListeners;


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
    target.style = "";
    
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
  
  /* if (e.clientX >= dropRect.left && e.clientX <= dropRect.right
   && e.clientY >= dropRect.top && e.clientY <= dropRect.bottom) { */
  if (isInDropRect(e.clientX, e.clientY)) {
    dropArea.classList.add(dropAreaHighlightClassName);
  } else {
    dropArea.classList.remove(dropAreaHighlightClassName);
  }
}
