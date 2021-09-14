const tableContainer = document.getElementById("grade-table-container");
const addSemesterButton = document.getElementById("grade-semester-add-button");
const tableHeaderLabels = ["Course", "ECTS", "Grade", ""];
const tableAlignments= ["left", "right", "right", "center"];
const tableInputPlaceholders = ["Course name", "ECTS", "Grade", ""];

function removeSemesterTableRow(buttonElement) {
  console.log(buttonElement);
  buttonElement.parentElement.parentElement.remove();
}

function addSemesterTableRow(table) {
  let tr = table.insertRow();
  tr.classList.add("content");
  for (let i = 0; i < 4; i++) {
    let td = tr.insertCell();
    td.classList.add(tableAlignments[i]);
    let childElement;
    
    if (i < 3) {
      childElement = document.createElement("input");
      childElement.type = "text";
      childElement.placeholder = tableInputPlaceholders[i];
    } else {
      childElement = document.createElement("button");
      childElement.classList.add("delete-button");
      childElement.onclick = () => removeSemesterTableRow(childElement);
    }
    td.appendChild(childElement);
  }
}

function createSemesterTable(parentElement) {
  let table = document.createElement("table"),
      tableWrapper = document.createElement("div"),
      tableAddRowButton = document.createElement("button"),
      colGroup = document.createElement("colgroup"),
      semesterHeader = document.createElement("h5");
  table.classList.add("grade-semester-table");
  tableAddRowButton.classList.add("grade-semester-table-button");
  tableAddRowButton.innerHTML = "Add new course";
  tableAddRowButton.onclick = () => addSemesterTableRow(table);
  tableWrapper.classList.add("grade-table-wrapper");
  semesterHeader.classList.add("grade-semester-title");
  semesterHeader.innerHTML = "TODO: Change me!";
  
  // Create columns for colgroup first
  for (let i = 0; i < 4; i++) {
    let col = document.createElement("col");
    if (i == 0) {
      col.classList.add("wide");
    } else {
      col.classList.add("narrow");
    }
    colGroup.appendChild(col);
  }
  table.appendChild(colGroup);
  
  // Create the table header and a single row
  let tableHeader = table.createTHead();
  for (let i = 0; i < 4; i++) {
    let th = document.createElement("th");
    th.classList.add(tableAlignments[i]);
    th.innerHTML = tableHeaderLabels[i];
    tableHeader.appendChild(th);
  }
  addSemesterTableRow(table);
  
  // Finally, add the table to the DOM
  tableWrapper.appendChild(semesterHeader);
  tableWrapper.appendChild(table);
  tableWrapper.appendChild(tableAddRowButton);
  parentElement.appendChild(tableWrapper);
}

function removeSemesterTable(index) {
  console.log("stub");
}

addSemesterButton.onclick = () => createSemesterTable(tableContainer);

// Create initial semester
createSemesterTable(tableContainer);
