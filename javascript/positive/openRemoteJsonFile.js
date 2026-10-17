/**
 * Fetch and load JSON data from a remote URL.
 *
 * This function retrieves JSON data from the specified URL using the native fetch API
 * and loads it into an object. If an exception occurs, it returns an object
 * containing an error message.
 *
 * @param {string} url - The URL of the remote JSON file.
 * @returns {Promise<object>} The JSON data loaded from the remote URL, or an error message in case of an exception.
 */
async function openRemoteJsonFile(url = '') {
    try {
        // Send a GET request to the specified URL
        const response = await fetch(url);
        
        // Check if the HTTP response status is OK (200-299)
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Parse and return the JSON data from the content
        const jsObject = await response.json();
        
        return jsObject;
    } catch (e) {
        // Return an object containing the error message
        return { error: e.message };
    }
}

// Example usage
// (async () => { const data = await openRemoteJsonFile('https://api.github.com/'); console.log(data); })();