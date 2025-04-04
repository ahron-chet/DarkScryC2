export async function side_bar_effect() {
  const sidebar = document.getElementById('sidebarMenu');
  const toggleBtn = document.getElementById('toggleSidebar');

  // 1) Toggle sidebar collapse
  toggleBtn.addEventListener('click', () => {
    sidebar.classList.toggle('collapsed');
  });

  // 2) If the sidebar is collapsed, expand on submenu link click
  //    ONLY if the link is inside #sidebarMenu
  sidebar.querySelectorAll('a[data-bs-toggle="collapse"]').forEach(link => {
    link.addEventListener('click', function (e) {
      if (sidebar.classList.contains('collapsed')) {
        e.preventDefault();
        sidebar.classList.remove('collapsed');
      }
    });
  });

  // 3) userToggle
  const userToggle = document.getElementById('side-bar-user-section');
  userToggle.addEventListener('click', function (e) {
    if (sidebar.classList.contains('collapsed')) {
      e.preventDefault();
      sidebar.classList.remove('collapsed');
      // Wait for transition
      sidebar.addEventListener('transitionend', function () {
        const dropdownToggle = userToggle.querySelector("h6.dropdown-toggle");
        if (dropdownToggle) {
          dropdownToggle.click();
        }
      }, { once: true });
    }
  });

  // 4) Submenu child links => only inside #sidebarMenu
  const childLinks = sidebar.querySelectorAll('.submenu .nav-link');
  childLinks.forEach(child => {
    child.addEventListener('click', function (e) {
      // Remove 'active' from everything
      const allLinks = sidebar.querySelectorAll('.nav-link');
      allLinks.forEach(l => l.classList.remove('active'));

      // Mark this child active
      child.classList.add('active');

      // Also set the parent's toggle link active
      const parentListItem = child.closest('.nav-item');
      if (parentListItem) {
        const parentToggle = parentListItem.querySelector(':scope > a.nav-link');
        if (parentToggle) {
          parentToggle.classList.add('active');
        }
      }
    });
  });

  // 5) Top-level nav links (again, scoping to #sidebarMenu)
  const topLevelNoChildLinks = sidebar.querySelectorAll(
    '.nav-item > .nav-link:not([data-bs-toggle="collapse"])'
  );
  topLevelNoChildLinks.forEach(link => {
    link.addEventListener('click', function () {
      // Remove 'active' from all links within #sidebarMenu only
      const allLinks = sidebar.querySelectorAll('.nav-link');
      allLinks.forEach(l => l.classList.remove('active'));

      // Mark this one active
      this.classList.add('active');
    });
  });
}


export function initAgentViewDropdowns() {
  const agentView = document.querySelector(".agent-view");
  if (!agentView) {
    console.warn("No .agent-view found. Skipping dropdown init.");
    return;
  }

  function closeSiblingMenus(liElement) {
    if (!liElement) return;
    const parentUl = liElement.closest(".dropdown-menu");
    if (!parentUl) return;

    parentUl.querySelectorAll(":scope > li.dropdown-submenu").forEach((siblingLi) => {
      if (siblingLi !== liElement) {
        const openSubmenu = siblingLi.querySelector(".dropdown-menu.show");
        if (openSubmenu) {
          openSubmenu.classList.remove("show");
          // Also remove .show from deeper descendants
          openSubmenu.querySelectorAll(".dropdown-menu.show").forEach((desc) => {
            desc.classList.remove("show");
          });
        }
      }
    });
  }

  function closeAllSubMenus() {
    agentView.querySelectorAll(".dropdown-menu.show").forEach((openMenu) => {
      openMenu.classList.remove("show");
    });
  }

  // 1) Toggle deeper submenus on click
  agentView.querySelectorAll(".dropdown-item.dropdown-toggle").forEach((toggleLink) => {
    toggleLink.addEventListener("click", (e) => {
      e.preventDefault();
      e.stopPropagation();

      const liParent = toggleLink.parentElement;
      const submenu = liParent?.querySelector(".dropdown-menu");
      if (!submenu) return;

      // If submenu is already open, close all => return to "beginning."
      if (submenu.classList.contains("show")) {
        closeAllSubMenus();
      } else {
        // Otherwise, normal behavior: close siblings, then open this submenu
        closeSiblingMenus(liParent);
        submenu.classList.add("show");
      }
    });
  });

  // 2) Clicking normal items closes the entire structure
  agentView.querySelectorAll(".dropdown-item:not(.dropdown-toggle)").forEach((normalItem) => {
    normalItem.addEventListener("click", () => {
      closeAllSubMenus();
    });
  });

  // 3) On top-level show, reset submenus
  document.querySelectorAll(".nav-item.dropdown").forEach((topLevel) => {
    topLevel.addEventListener("show.bs.dropdown", () => {
      closeAllSubMenus();
    });
  });
}
