const urlInput = document.getElementById("url-input");
const urlOutput = document.getElementById("url-output");
const decodeButton = document.getElementById("decode-btn");
const clipboardButton = document.getElementById("copy-clipboard-btn");

function decodeURL(url) {
  urlOutput.value = decodeURIComponent(url);
}

decodeButton.onclick = () => decodeURL(urlInput.value);
clipboardButton.onclick = () => navigator.clipboard.writeText(urlOutput.value).then(
    () => console.log("Successfully copied URL to clipboard."),
    () => console.log("Failure - could not copy URL to clipboard.")
);

