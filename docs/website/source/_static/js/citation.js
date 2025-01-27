async function loadOptions() {
  try {
    const response = await fetch('https://raw.githubusercontent.com/RepoDynamics/PyPackIT/refs/heads/main/docs/website/source/_static/data/csl_styles.json');
    if (!response.ok) throw new Error(`Failed to load options: ${response.statusText}`);
    const optionsData = await response.json();

    const dropdown = document.getElementById('api-dropdown');

    // Clear existing options if any
    dropdown.innerHTML = '<option value="" disabled selected>Select an option</option>';

    // Populate dropdown with options
    for (const [key, value] of Object.entries(optionsData)) {
      // Create the display text based on the array content
      let displayText = value.length === 1
        ? value[0]
        : `${value[0]} (${value[1]})`;

      const optionElement = document.createElement('option');
      optionElement.value = key; // Use the key as the value sent to the API
      optionElement.textContent = displayText; // Display the constructed text
      dropdown.appendChild(optionElement);
    }

  } catch (error) {
    console.error(error);
    const resultDiv = document.getElementById('api-response');
    resultDiv.textContent = `Error loading options: ${error.message}`;
  }
}

async function fetchAPI() {
  const dropdown = document.getElementById('api-dropdown');
  const resultDiv = document.getElementById('api-response');
  const selectedKey = dropdown.value;

  if (!selectedKey) {
    resultDiv.textContent = "Please select an option.";
    return;
  }

  // API request construction
    const apiUrl = `https://doi.org/10.5281/zenodo.14744153`;
    const headers = {'accept': `text/x-bibliography; style=${selectedOption}`};

  try {
    resultDiv.textContent = 'Loading...';
    const response = await fetch(apiUrl, {
      method: 'GET',
      headers: headers
    });
    if (!response.ok) throw new Error(`Error: ${response.status} ${response.statusText}`);
    const data = await response.text();
    resultDiv.textContent = data;
  } catch (error) {
    resultDiv.textContent = `Error: ${error.message}`;
  }
}


// Load options when the page loads
window.onload = loadOptions;
