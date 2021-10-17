![url-decoder](../.github/url-decoder.png)
# 🌐 URL decoder
**Languages used**: HTML, CSS, JavaScript

**Libraries used**: None

Occasionally, you'll stumble upon a URL with a bunch of strings like ``%29``
or ``%3A``. These strings were created from
[Percent-encoding](https://en.wikipedia.org/wiki/Percent-encoding), which allows
otherwise illegal characters to be used in URLs. An example would be ``+``,
which is encoded as ``%2B``. Trying to decode a URL with dozens of these symbols
is quite a headache, which this URL decoder aims to solve. While you could also
just go into your browser console and use ``decodeURIComponent`` to decode a
URL, I decided to create this little app as practice and to make this whole
process a bit more comfortable.

## Usage
Simply open ``url-decoder.html`` with your favorite browser.

From there, enter a URL with percent-encoding into the text area. Then, use the
**Decode** button to decode the URL you've entered. Once decoded, the output
appears in a text area at the bottom of the page. Copy the URL using the button
on the right side of the text area and do with it as you wish.
