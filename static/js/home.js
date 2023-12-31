function toggleFooter() {
  const footer = document.getElementById('footer');
  
  // Check the current state of the footer and toggle it
  if (footer.style.transform === 'translateY(100%)') {
      footer.style.transform = 'translateY(0)'; // Slide in to become visible
  } else {
      footer.style.transform = 'translateY(100%)'; // Slide out to become non-visible
  }
}
function logout(){
  if (confirm("Are you sure you want to logout?")){
    window.location.href="/";
  }
}

window.onload = function() {
  const footer = document.getElementById('footer');
  footer.style.transform = 'translateY(100%)'; // Ensure it starts out of view
};

function toggleSidebar() {
  var sidebar = document.getElementById('sidebar');
  sidebar.classList.toggle('sidebar-responsive');
}

// If sidebar-responsive is the class that shows the sidebar, this function will work.
// Ensure that the sidebar has the correct styles for the sidebar-responsive class in your CSS.

document.addEventListener("DOMContentLoaded", function () {
  // Attach the toggle function to the menu icon and close icon
  document.querySelector('.menu-icon').addEventListener('click', toggleSidebar);
  document.querySelector('.sidebar-title .material-symbols-outlined').addEventListener('click', toggleSidebar);

  // Add functionality for sidebar list items to toggle content
  var sidebarListItems = document.querySelectorAll('.sidebar-list-item');
  sidebarListItems.forEach(function (item) {
    item.addEventListener('click', function () {
      // Assuming that you have the data-target attribute set correctly on your list items
      var contentId = item.getAttribute('data-target');
      var contentDivs = document.querySelectorAll('.content-div');

      contentDivs.forEach(function (div) {
        div.style.display = div.id === contentId ? 'block' : 'none';
      });
    });
  });

});