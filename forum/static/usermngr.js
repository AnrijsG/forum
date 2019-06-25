$.ajaxSetup({
 beforeSend: function(xhr, settings) {
     function getCookie(name) {
         var cookieValue = null;
         if (document.cookie && document.cookie != '') {
             var cookies = document.cookie.split(';');
             for (var i = 0; i < cookies.length; i++) {
                 var cookie = jQuery.trim(cookies[i]);
                 // Does this cookie string begin with the name we want?
                 if (cookie.substring(0, name.length + 1) == (name + '=')) {
                     cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                     break;
                 }
             }
         }
         return cookieValue;
     }
     if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
         // Only send the token to relative URLs i.e. locally.
         xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
     }
 }
});
var userId = 0;

function change(x) {
    userId = x;
}

$(function () {
    $("#save_changes").click( function () {
        var ModeratorChecked = $("#ModeratorCheckbox").is(":checked");
        var AdministratorChecked = $("#AdministratorCheckbox").is(":checked");
        $.post("/changeRoles", JSON.stringify({moderator: ModeratorChecked, administrator: AdministratorChecked, user_id: userId}), function() {
            location.reload();
        });
    });
})