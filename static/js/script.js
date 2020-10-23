/* Toggle show on sidebar/custom view */

// const dashToggle = document.querySelector("#sidebar-collapse");

// dashToggle.addEventListener('click', (event) => {
//     event.currentTarget.classList.toggle('active');
//     console.log(event.currentTarget);
// });


window.addEventListener('click', (event) => console.log(event.target));

$(".custom-menu").click(function (e) {
    $("#user-dashboard").toggleClass("active");
    console.log(e);
  });