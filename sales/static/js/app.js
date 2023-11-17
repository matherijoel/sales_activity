// Message/Notification timer

var message_timeout = document.getElementById("message-timer");

setTimeout(function()

{

    message_timeout.style.display = "none";


}, 5000);

// static/js/app.js
$(document).ready(function(){
    $('.datepicker').datepicker({
        dateFormat: 'dd/mm/yy'
    });
});