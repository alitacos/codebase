// Installieren mit: npm install pdfjs-dist
const pdfjsLib = require('pdfjs-dist');

/**
 * Fetch and load a PDF document from a remote URL into memory.
 * 
 * @param {string} url - The URL of the remote PDF file.
 * @returns {Promise<object>} The PDF document object (PDFDocumentProxy).
 */
async function openRemotePdfFileViaPdfjsDist(url = '') {
    try {
        // 1. PDF-Daten als ArrayBuffer (Binärdaten im Speicher) herunterladen
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const arrayBuffer = await response.arrayBuffer();

        // 2. Die Binärdaten direkt an pdfjs-dist übergeben (entspricht stream=data)
        const loadingTask = pdfjsLib.getDocument({ data: arrayBuffer });
        const pdfDocument = await loadingTask.promise;

        return pdfDocument;
    } catch (e) {
        return { error: e.message };
    }
}

// Beispiel-Aufruf
// (async () => { const pdf = await openRemotePdfFileViaPdfjsDist('https://arxiv.org/pdf/1706.03762'); if (pdf.error) { console.error("Fehler:", pdf.error); } else { console.log(`PDF erfolgreich geladen. Anzahl der Seiten: ${pdf.numPages}`); } })();