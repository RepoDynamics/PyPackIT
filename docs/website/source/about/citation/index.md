# Citation

|{{ helper.create_citation() }}|

<div>
  <label for="api-dropdown">Choose an option:</label>
  <select id="api-dropdown" onchange="fetchAPI()">
    <option value="" disabled selected>Select an option</option>
    <option value="option1">Option 1</option>
    <option value="option2">Option 2</option>
    <option value="option3">Option 3</option>
  </select>
</div>

<div id="api-response" style="margin-top: 20px; padding: 10px; border: 1px solid #ccc; border-radius: 5px; white-space: pre-wrap;">
  <!-- API response will be displayed here -->
</div>