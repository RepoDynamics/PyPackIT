async function loadOptions() {
  try {
    console.log('Fetching options JSON...');
    const response = await fetch('https://raw.githubusercontent.com/RepoDynamics/PyPackIT/main/docs/website/source/_static/data/csl_styles.json');
    if (!response.ok) throw new Error(`Failed to load options: ${response.statusText}`);

    console.log('Response received.');
    const optionsData = await response.json();
    console.log('Options Data:', optionsData);

    const dropdown = document.getElementById('api-dropdown');

    // Clear existing options if any
    dropdown.innerHTML = '<option value="" disabled selected>Select an option</option>';

    // Sort optionsData before populating the dropdown
    const sortedEntries = Object.entries(optionsData).sort(([, valueA], [, valueB]) => {
      const textA = valueA.length === 1 ? valueA[0] : `${valueA[0]} (${valueA[1]})`;
      const textB = valueB.length === 1 ? valueB[0] : `${valueB[0]} (${valueB[1]})`;
      return textA.localeCompare(textB); // Sort alphabetically
    });

    // Populate dropdown with sorted options
    for (const [key, value] of sortedEntries) {
      console.log('Processing key:', key, 'value:', value);
      let displayText = value.length === 1
        ? value[0]
        : `${value[0]} (${value[1]})`;

      const optionElement = document.createElement('option');
      optionElement.value = key; // Use the key as the value sent to the API
      optionElement.textContent = displayText; // Display the constructed text
      dropdown.appendChild(optionElement);
    }

  } catch (error) {
    console.error('Error in loadOptions:', error);
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

  const apiUrl = `https://doi.org/10.5281/zenodo.14744153`;
  const headers = { 'accept': `text/x-bibliography; style=${selectedKey}` };

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
window.addEventListener('load', loadOptions);
