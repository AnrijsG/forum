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

function isNotBlank(value) {
    return typeof value !== "undefined" && value !== null && (typeof value !== "string" || value.trim() !== "");
}

function newPost(threadId, text) {
    if(isNotBlank(text)) {
        $.post(threadId + "/post", JSON.stringify({text: text}), function() {
            alert("success")
        });
    }else {
        alert("a");
    }
}
$(function() {
   $("#post_button").click(function() {
        newPost(threadId, $("#post").val())
   });
});