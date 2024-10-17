// Change the image source of themed images based on the current theme.
// Reference: https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/light-dark.html#define-custom-javascript-to-react-to-theme-changes

function updateImagesBasedOnTheme() {
    // Check if the current theme is dark
    const dark = document.documentElement.dataset.theme == 'dark';
    // Get all elements with both "dark-light" and "themed" classes
    const elements = document.querySelectorAll('.dark-light.themed');
    // Regular expression to find "_light" or "_dark" right before the file extension
    const regex = /_(light|dark)(\.[a-zA-Z]+)$/;
    // Loop through each image element
    elements.forEach(function(element) {
        // Check if the src matches the regular expression
        if (element.src) {
            let src = element.src;
            // Check if the src matches the regular expression
            let match = src.match(regex);
            if (match) {
                // Replace "_light" with "_dark" if the theme is dark, and vice versa
                element.src = src.replace(match[1], dark ? 'dark' : 'light');
            }
        } else {
            // Log element details if it doesn't have a src
            console.log("Element without src detected:", element);
        }
    });
}

// Run the function on page load to set the correct images
updateImagesBasedOnTheme();
// Observe changes to the 'data-theme' attribute
var observer = new MutationObserver(function(mutations) {
    updateImagesBasedOnTheme();  // Run the function whenever the theme changes
});
// Start observing changes to the 'data-theme' attribute
observer.observe(document.documentElement, {attributes: true, attributeFilter: ['data-theme']});
