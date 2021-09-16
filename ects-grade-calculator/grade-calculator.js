const tableContainer = document.getElementById("grade-table-container");
const addSemesterButton = document.getElementById("grade-semester-add-button");
const tableHeaderLabels = ["Course", "ECTS", "Grade", ""];
const tableAlignments= ["left", "right", "right", "center"];
const tableInputPlaceholders = ["Course name", "ECTS", "Grade", ""];
const tableClassIdentifiers = ["course", "ects", "grade"];
const tableWidths = ["wide", "narrow", "narrow", "narrow"];

const ectsTotal = document.getElementById("ects-total");
const pointsTotal = document.getElementById("points-total");
const gradeResult = document.getElementById("grade-overall-result");
const gradeResultTable = document.getElementById("grade-results-table");
const resultButton = document.getElementById("grade-results-button");
const resultCircle = document.getElementById("grade-result-circle-svg");
const resultCircleFull = 100 * (2 / 3);
let resultCircleCircumference;

/**
 * Adds a new semester to the results table.
 *
 * @param {string} semesterTitle  Title of the semester that is to be added.
 */
function addSemesterResultsRow(semesterTitle) {
  let tr = gradeResultTable.insertRow();
  let keyTd = tr.insertCell();
  keyTd.classList.add("left", "span-label");
  keyTd.innerHTML = semesterTitle;
  let valueTd = tr.insertCell();
  valueTd.classList.add("right", "span-value");
}

/**
 * Removes a course from a semester table based on the triggering button
 * element.
 *
 * @param {object} buttonElement  Button element that triggered deletion.
 */
function removeSemesterTableRow(buttonElement) {
  buttonElement.parentElement.parentElement.remove();
}

/**
 * Adds a new row to the specified semester table.
 *
 * @param {object} table  Table the new row should be appended to
 */
function addSemesterTableRow(table) {
  let tr = table.insertRow();
  tr.classList.add("content");
  
  // Add table cells to the newly created table row
  for (let i = 0; i < 4; i++) {
    let td = tr.insertCell();
    td.classList.add(tableAlignments[i]);
    let childElement;
    
    // Add input elements to each table cell, except for the last one, which
    // is a button to delete the corresponding row
    if (i < 3) {
      childElement = document.createElement("input");
      childElement.type = "text";
      childElement.placeholder = tableInputPlaceholders[i];
      childElement.classList.add(tableClassIdentifiers[i]);
    } else {
      childElement = document.createElement("button");
      childElement.classList.add("delete-button");
      childElement.onclick = () => removeSemesterTableRow(childElement);
    }
    td.appendChild(childElement);
  }
}

/**
 * Creates a table for a new semester, appended to the specified parent element.
 *
 * @param {object} parentElement  DOM element the table should be appended to
 */
function createSemesterTable(parentElement) {
  // Create all required top-level elements
  let table = document.createElement("table"),
      tableWrapper = document.createElement("div"),
      tableAddRowButton = document.createElement("button"),
      colGroup = document.createElement("colgroup"),
      semesterHeader = document.createElement("h5");
  const semesterTitle = "TODO: Change me!";
  
  // Perform setup operations, such as adding CSS classes
  table.classList.add("grade-semester-table");
  tableAddRowButton.classList.add("grade-semester-table-button");
  tableAddRowButton.innerHTML = "Add new course";
  tableAddRowButton.onclick = () => addSemesterTableRow(table);
  tableWrapper.classList.add("grade-table-wrapper");
  semesterHeader.classList.add("grade-semester-title");
  semesterHeader.innerHTML = semesterTitle;
  
  // Create columns for colgroup first
  for (let i = 0; i < 4; i++) {
    let col = document.createElement("col");
    col.classList.add(tableWidths[i]);
    colGroup.appendChild(col);
  }
  table.appendChild(colGroup);
  
  // Create the table header
  let tableHeader = table.createTHead();
  for (let i = 0; i < 4; i++) {
    let th = document.createElement("th");
    th.classList.add(tableAlignments[i]);
    th.innerHTML = tableHeaderLabels[i];
    tableHeader.appendChild(th);
  }
  
  // Add new rows for the newly created semester
  addSemesterTableRow(table);
  addSemesterResultsRow(semesterTitle);
  
  // Finally, append the child elements to the table and add
  // the table to the DOM
  tableWrapper.appendChild(semesterHeader);
  tableWrapper.appendChild(table);
  tableWrapper.appendChild(tableAddRowButton);
  parentElement.appendChild(tableWrapper);
}

/**
 * Removes the specified semester table.
 */
function removeSemesterTable(index) {
  console.log("stub");
}

/**
 * Setup the progress circle for animation by setting strokeDashoffset and
 * strokeDasharray to the circumference of the circle.
 */
function setupProgressCircle() {
  const radius = resultCircle.r.baseVal.value;
  resultCircleCircumference = radius * 2 * Math.PI;
  resultCircle.style.strokeDashoffset = `${resultCircleCircumference}`;
  resultCircle.style.strokeDasharray = `${resultCircleCircumference} ${resultCircleCircumference}`;
}

/**
 * Sets the progress of the progress circle in percent.
 *
 * @param {number} percent  Progress in percent
 */
function setProgress(percent) {
  const offset = resultCircleCircumference - percent / 100 * resultCircleCircumference;
  resultCircle.style.transition = "0.35s stroke-dashoffset";
  resultCircle.style.strokeDashoffset = offset;
}

/**
 * Calculates the final grade based on the semester tables that the user
 * created. Sets the values of the result DOM elements accordingly.
 */
function calculateGrade() {
  let ectsElements = document.getElementsByClassName("ects");
  let gradeElements = document.getElementsByClassName("grade");
  let totalEcts = 0, totalPoints = 0;
  
  // Loop through all courses and add ECTS as well as points to the total
  for (let i = 0; i < ectsElements.length; i++) {
    const ects = parseFloat(ectsElements[i].value);
    const grade = parseFloat(gradeElements[i].value);
    
    // Ignore incomplete or invalid rows
    if (!(isNaN(ects) || isNaN(grade))) {
      totalEcts += ects;
      totalPoints += ects * grade;
    }
  }
  
  // Update all result elements accordingly
  const result = totalPoints / totalEcts;
  setProgress((100 - (100 / 3) * (result - 1)) * 0.01 * resultCircleFull);
  ectsTotal.innerHTML = totalEcts;
  pointsTotal.innerHTML = totalPoints;
  gradeResult.innerHTML = +result.toFixed(2);
}

// Setup everything else
addSemesterButton.onclick = () => createSemesterTable(tableContainer);
resultButton.onclick = () => calculateGrade();
createSemesterTable(tableContainer);
setupProgressCircle();
