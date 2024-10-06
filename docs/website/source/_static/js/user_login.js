// User login popup and link updating

document.addEventListener("DOMContentLoaded", function() {

    const Dialog = document.getElementById('user-login-dialog');
    const Form = document.getElementById('user-login-form');

    // Function to load saved repository info
    const loadUserLogin = () => {
        const defaultRepoOwner = "RepoDynamics";
        const defaultRepoName = "PyPackIT-Example";
        const defaultRepoBranch = "main";
        const savedRepoOwner = localStorage.getItem('userRepoOwner') || defaultRepoOwner;
        const savedRepoName = localStorage.getItem('userRepoName') || defaultRepoName;
        const savedRepoBranch = localStorage.getItem('userRepoBranch') || defaultRepoBranch;
        document.getElementById('user-repo-owner').value = savedRepoOwner;
        document.getElementById('user-repo-name').value = savedRepoName;
        document.getElementById('user-repo-branch').value = savedRepoBranch;
        updateUserRepoLinks(savedRepoOwner, savedRepoName, savedRepoBranch);
    };

    // Function to show the repository popup
    const showDialog = (event) => {
        event.stopPropagation(); // Stop the click from affecting other buttons
        loadUserLogin();
        Dialog.showModal();
    };

    // Function to update all repository-related links
    const updateUserRepoLinks = (repoOwner, repoName, repoBranch) => {
        // add icon to all link content
        document.querySelectorAll('[class^="user-link-repo"]').forEach(link => {
            link.textContent = `<i class="fa-brands fa-square-github"></i> ` + link.textContent;
        }
        // update links
        document.querySelectorAll(".user-link-repo-home").forEach(link => {
            link.href = `https://github.com/${repoOwner}/${repoName}`;
        });
        document.querySelectorAll(".user-link-repo-actions").forEach(link => {
            link.href = `https://github.com/${repoOwner}/${repoName}/actions`;
        });
        document.querySelectorAll(".user-link-repo-commits").forEach(link => {
            link.href = `https://github.com/${repoOwner}/${repoName}/commits/${repoBranch}`;
        });
        document.querySelectorAll(".user-link-repo-readme").forEach(link => {
            link.href = `https://github.com/${repoOwner}/${repoName}/blob/${repoBranch}/README.md`;
        });
        document.querySelectorAll(".user-link-repo-cc").forEach(link => {
            link.href = `https://github.dev/${repoOwner}/${repoName}/blob/${repoBranch}/.control`;
        });
        document.querySelectorAll(".user-link-repo-cc-proj").forEach(link => {
            link.href = `https://github.dev/${repoOwner}/${repoName}/blob/${repoBranch}/.control/proj.yaml`;
        });
        document.querySelectorAll(".user-link-repo-logo").forEach(link => {
            link.href = `https://github.com/${repoOwner}/${repoName}/blob/${repoBranch}/docs/media/logo`;
        });
        document.querySelectorAll(".user-link-repo-settings-secrets-actions-new").forEach(link => {
            link.href = `https://github.com/${repoOwner}/${repoName}/settings/secrets/actions/new`;
        });
        document.querySelectorAll(".user-link-repo-org-settings-actions").forEach(link => {
            link.href = `https://github.com/organizations/${repoOwner}/settings/actions`;
    };

    // Attach click handler to all instances of the login button
    document.querySelectorAll(".user-login-button").forEach((btn) => {
        btn.onclick = showDialog;
        // Detect when the dialog is closed and blur the button
        Dialog.addEventListener('close', function() {
            btn.blur();
        });
    });

    // Close the popup if the user clicks outside the dialog
    Dialog.addEventListener('click', function(event) {
        const rect = Dialog.getBoundingClientRect();
        if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) {
            Dialog.close();
        }
    });

    // Form submission
    Form.addEventListener('submit', function(event) {
        event.preventDefault();
        const userRepoOwner = document.getElementById('user-repo-owner').value;
        const userRepoName = document.getElementById('user-repo-name').value;
        const userRepoBranch = document.getElementById('user-repo-branch').value;
        localStorage.setItem('userRepoOwner', userRepoOwner);
        localStorage.setItem('userRepoName', userRepoName);
        localStorage.setItem('userRepoBranch', userRepoBranch);
        updateUserRepoLinks(userRepoOwner, userRepoName, userRepoBranch);
        Dialog.close();
    });

    // Initialize and update links on page load
    loadUserLogin();

});