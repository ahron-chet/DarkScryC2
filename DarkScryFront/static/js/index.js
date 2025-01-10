const sidebar = document.getElementById('sidebarMenu');
const toggleBtn = document.getElementById('toggleSidebar');

// 1) Toggle sidebar on button click
toggleBtn.addEventListener('click', () => {
    sidebar.classList.toggle('collapsed');
});

// 2) Expand sidebar if collapsed & a submenu link is clicked
document.querySelectorAll('a[data-bs-toggle="collapse"]').forEach(link => {
    link.addEventListener('click', function(e) {
        if (sidebar.classList.contains('collapsed')) {
            e.preventDefault();
            sidebar.classList.remove('collapsed');
        }
    });
});


const userToggle = document.getElementById('side-bar-user-section');
userToggle.addEventListener('click', function(e) {
    if (sidebar.classList.contains('collapsed')) {
        e.preventDefault(); // Prevent default behavior
        sidebar.classList.remove('collapsed'); // Start expanding the sidebar

        // Wait for the transition to complete
        sidebar.addEventListener(
            'transitionend',
            function() {
                // Programmatically trigger the dropdown toggle after transition
                const dropdownToggle = userToggle.querySelector("h6.dropdown-toggle");
                if (dropdownToggle) {
                    dropdownToggle.click(); // Simulate a click to expand the dropdown
                }
            }, {
                once: true
            } // Ensure this listener is executed only once
        );
    }
});



const childLinks = document.querySelectorAll('.submenu .nav-link');

childLinks.forEach(child => {
    child.addEventListener('click', function(e) {
        // Remove 'active' from everything
        const allLinks = document.querySelectorAll('.nav-link');
        allLinks.forEach(l => l.classList.remove('active'));

        // Set this child link active
        child.classList.add('active');

        // Also set the parent link (the <a> that toggles the submenu) active
        const parentListItem = child.closest('.nav-item');
        if (parentListItem) {
            const parentToggle = parentListItem.querySelector(':scope > a.nav-link');
            if (parentToggle) {
                parentToggle.classList.add('active');
            }
        }
    });
});


const topLevelNoChildLinks = document.querySelectorAll(
    '.nav-item > .nav-link:not([data-bs-toggle="collapse"])'
);
topLevelNoChildLinks.forEach(link => {
    link.addEventListener('click', function() {
        // Remove 'active' from all
        const allLinks = document.querySelectorAll('.nav-link');
        allLinks.forEach(l => l.classList.remove('active'));

        // Set this one active
        this.classList.add('active');
    });
});