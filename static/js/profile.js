/* Toggle dashboard view on smaller devices */
window.onload = function() {
  document.getElementById('dashboard-toggle').onclick = function() {
    document.getElementById('user-dashboard').classList.toggle('active');
  };
}


