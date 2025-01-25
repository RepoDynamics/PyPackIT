// Change the image source of themed images based on the current theme.
// Reference: https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/light-dark.html#define-custom-javascript-to-react-to-theme-changes

function updateImagesBasedOnTheme() {
    // Check if the current theme is dark
    const dark = document.documentElement.dataset.theme == 'dark';

    // ---- Update <img> elements with "dark-light" and "themed" classes ----
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

    // ---- Update <picture> elements ----
    const pictures = document.querySelectorAll("picture");
    pictures.forEach((picture) => {
        const img = picture.querySelector("img");
        if (!img) return;
        let dataLightSrc = picture.getAttribute("data-light-src");
        let dataDarkSrc = picture.getAttribute("data-dark-src");
        const sources = picture.querySelectorAll("source");
        if (!dataLightSrc || !dataDarkSrc) {
            // If not stored, iterate over <source> elements to identify light/dark URLs
            sources.forEach((source) => {
                const isLightScheme = source.media.includes("(prefers-color-scheme: light)");
                if (isLightScheme) {
                    dataLightSrc = source.srcset;
                    picture.setAttribute("data-light-src", dataLightSrc); // Store light URL
                } else {
                    dataDarkSrc = source.srcset;
                    picture.setAttribute("data-dark-src", dataDarkSrc); // Store dark URL
                }
            });
        }
        // Based on the current theme, select the appropriate source URL
        const newSrc = dark ? dataDarkSrc : dataLightSrc;
        if (newSrc) {
            // Update all <source> elements with the selected URL
            sources.forEach((source) => {
                source.srcset = newSrc;
            });
            // Force the browser to re-evaluate the <picture>
            const img = picture.querySelector("img");
            if (img) {
                const currentSrc = img.src;
                img.src = ""; // Clear current src
                img.src = currentSrc; // Restore it to force re-render
            }
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
