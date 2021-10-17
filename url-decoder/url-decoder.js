const urlInput = document.getElementById("url-input");
const urlOutput = document.getElementById("url-output");
const decodeButton = document.getElementById("decode-btn");
const clipboardButton = document.getElementById("copy-clipboard-btn");
const queryParamTable = document.getElementById("url-query-params-table");

/**
 * Decodes the provided URL and adjusts all content accordingly.
 * 
 * @param {String}  url  URL as string.
 */
function decodeURL(url) {
  urlOutput.value = decodeURIComponent(url);
  const tableRows = document.querySelectorAll("#url-query-params-table tr");
  for (let tableRow of tableRows) {
    tableRow.remove();
  }
  
  // Only attempt to find query parameters if a question mark symbol is found
  const urlParamIndex = url.indexOf("?");
  if (urlParamIndex != -1) {
    // Search for query parameters starting from the first symbol after the
    // question mark - otherwise, the base URL will be included in the first
    // key as well
    const searchParams = new URLSearchParams(
      url.substring(urlParamIndex + 1, url.length)
    );
    searchParams.forEach((value, key) => {
      let tr = queryParamTable.insertRow();      
      let tdKey = tr.insertCell();
      let tdValue = tr.insertCell();
      tdKey.classList.add("table-key-cell");
      tdValue.classList.add("table-value-cell");
      tdKey.innerHTML = key;
      
      // Wrap URLs in an <a> element, if possible
      try {
        const queryParamURL = new URL(value);
        let linkElement = document.createElement("a");
        linkElement.href = queryParamURL.href;
        linkElement.innerHTML = value;
        tdValue.appendChild(linkElement);
      } catch (err) {
        // Not a valid URL, just put in the inner HTML
        tdValue.innerHTML = value;
      }
    });
  }
}

decodeButton.onclick = () => decodeURL(urlInput.value);
clipboardButton.onclick = () => navigator.clipboard.writeText(urlOutput.value).then(
    () => console.log("Successfully copied URL to clipboard."),
    () => console.log("Failure - could not copy URL to clipboard.")
);

