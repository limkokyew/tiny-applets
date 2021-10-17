const urlInput = document.getElementById("url-input");
const urlOutput = document.getElementById("url-output");
const decodeButton = document.getElementById("decode-btn");
const clipboardButton = document.getElementById("copy-clipboard-btn");
const queryParamTable = document.getElementById("url-query-params-table");

function decodeURL(url) {
  urlOutput.value = decodeURIComponent(url);
  const tableRows = document.querySelectorAll("#url-query-params-table tr");
  for (let tableRow of tableRows) {
    tableRow.remove();
  }
  
  const urlParamIndex = url.indexOf("?");
  if (urlParamIndex != -1) {
    const searchParams = new URLSearchParams(
      url.substring(urlParamIndex + 1, url.length)
    );
    searchParams.forEach((value, key) => {
      let tr = queryParamTable.insertRow();      
      let tdKey = tr.insertCell();
      let tdValue = tr.insertCell();
      tdKey.classList.add("table-key-cell");
      tdKey.innerHTML = key;
      tdValue.innerHTML = value;
    });
  }
}

decodeButton.onclick = () => decodeURL(urlInput.value);
clipboardButton.onclick = () => navigator.clipboard.writeText(urlOutput.value).then(
    () => console.log("Successfully copied URL to clipboard."),
    () => console.log("Failure - could not copy URL to clipboard.")
);

