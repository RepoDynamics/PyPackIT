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
        selected: false, // Default: not selected
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

    // Automatically select "apa" if it exists
    const apaOption = preparedOptions.find(option => option.value === 'apa');
    if (apaOption) {
      dropdown.value = 'apa'; // Set "apa" as selected in the dropdown
      await fetchAPI(); // Fetch and display the API response for "apa"
    } else {
      console.warn('The "apa" style was not found in the options.');
    }
  } catch (error) {
    console.error('Error in loadOptions:', error);
    const resultDiv = document.getElementById('api-rendered-response');
    resultDiv.innerHTML = `Error loading options: ${error.message}`;
  }
}

async function fetchAPI() {
  const dropdown = document.getElementById('api-dropdown');
  const apiRawResponseDiv = document.getElementById('api-raw-response'); // The wrapper <div>
  const preElement = apiRawResponseDiv.querySelector('pre'); // The <pre> inside the <div>
  const renderedResultDiv = document.getElementById('api-rendered-response');
  const selectedKey = dropdown.value;

  if (!selectedKey) {
    if (preElement) preElement.textContent = "Please select an option.";
    renderedResultDiv.innerHTML = ""; // Clear previous rendered HTML
    return;
  }

  const apiUrl = `https://doi.org/10.5281/zenodo.14744153`;
  const headers = { 'accept': `text/x-bibliography; style=${selectedKey}` };

  try {
    if (preElement) preElement.textContent = 'Loading...';
    renderedResultDiv.innerHTML = ""; // Clear previous rendered HTML

    const response = await fetch(apiUrl, {
      method: 'GET',
      headers: headers,
    });
    if (!response.ok) throw new Error(`Error: ${response.status} ${response.statusText}`);

    const data = await response.text();

    // Display the raw HTML response inside the <pre> element
    if (preElement) {
      preElement.textContent = data;
    }

    // Display the rendered HTML response
    renderedResultDiv.innerHTML = data;
  } catch (error) {
    if (preElement) preElement.textContent = `Error: ${error.message}`;
    renderedResultDiv.innerHTML = ""; // Clear previous rendered HTML
  }
}

// Load options and prepopulate the divs when the page loads
window.addEventListener('load', loadOptions);
