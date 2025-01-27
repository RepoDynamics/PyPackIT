async function loadOptions() {
  try {
    console.log('Fetching options JSON...');
    const response = await fetch('https://raw.githubusercontent.com/RepoDynamics/PyPackIT/main/docs/website/source/_static/data/csl_styles.json');
    if (!response.ok) throw new Error(`Failed to load options: ${response.statusText}`);

    console.log('Response received.');
    const optionsData = await response.json();
    console.log('Options Data:', optionsData);

    const dropdown = document.getElementById('api-dropdown');

    // Sort optionsData before populating the dropdown
    const sortedEntries = Object.entries(optionsData).sort(([, valueA], [, valueB]) => {
      const textA = valueA.length === 1 ? valueA[0] : `${valueA[0]} (${valueA[1]})`;
      const textB = valueB.length === 1 ? valueB[0] : `${valueB[0]} (${valueB[1]})`;
      return textA.localeCompare(textB); // Sort alphabetically
    });

    // Prepare options in a batch to add them all at once
    const preparedOptions = sortedEntries.map(([key, value]) => {
      const displayText = value.length === 1
        ? value[0]
        : `${value[0]} (${value[1]})`;

      return {
        value: key, // Key as the value sent to the API
        label: displayText, // Display text for the dropdown
        selected: false,
      };
    });

    // Initialize Choices.js once and add all options at once
    const choices = new Choices(dropdown, {
      searchEnabled: true,
      itemSelectText: '',
      placeholder: true,
      noResultsText: 'No options found',
      removeItemButton: false,
    });

    // Add all prepared options in one call
    choices.setChoices(preparedOptions, 'value', 'label', false);

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
