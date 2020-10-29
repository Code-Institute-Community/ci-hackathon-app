$(document).ready(function(){
    $( "#accordion" ).accordion();
});

/* Toggle dashboard view on smaller devices */
$(".custom-menu").click(function (e) {
    $("#user-dashboard").toggleClass("active");
    console.log(e);
  });
