(function() {
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

    function getThreads(sectionId, offset) {
        $.get("/sections/" + sectionId + "/threads?limit=5&offset=" + offset)
            .done(function(threads) {
                    addThreads(sectionId, threads);
                }
            )
    }

    function isNotBlank(value) {
        return typeof value !== "undefined" && value !== null && (typeof value !== "string" || value.trim() !== "");
    }


    var sections = {};

    function newThread(sectionId, title, text) {
        if(isNotBlank(title) && isNotBlank(text)) {
            $.post("/sections/" + sectionId + "/threads", JSON.stringify({title: title, text: text}), function(newThreadId) {
                window.location = "/thread/" + newThreadId["id"];
            });
        }else {
            //alert("Please fill all the fields!");
             $('.popover-dismiss').popover({
                 trigger: 'focus'
            })
        }
    }

    function addThreads(sectionId, threads) {

        if (!sections[sectionId]) {
            sections[sectionId] = threads;
        } else {
            sections[sectionId] = sections[sectionId].concat(threads);
        }
        var container = $("#container-" + sectionId);
        for (var i in threads) {
            var thread = threads[i];
            console.log(thread);
            var dom = $("<div class='card-body border'><a href='/thread/" + thread.id + "'>" + thread.title + "</a><br><p class='text-right'>Created by: " + "<a href = '/u/ " + thread.first_post['author'] + "'>" + thread.author + "</a>" + "</p></div>");
            container.append(dom);
        }
    }

    $(function() {
        $('[data-toggle="popover"]').popover()
        $("#post_thread").click(function() {
            let sectionId = $("a[data-toggle='tab'].active").attr("data-section-id");
            newThread(sectionId, $("#thread_title").val(), $("#post").val());
        });
        $("a[data-toggle='tab']").each(function() {
            var sectionId = this.attributes["data-section-id"].value;
            var jq = $(this);
            if (jq.hasClass("active")) {
                getThreads(sectionId, 0);
            }
            jq.on("shown.bs.tab", function() {
                if (!sections[sectionId]) {
                    getThreads(sectionId, 0);
                }
            });
            $("#load-more-" + sectionId).click(function() {
                getThreads(sectionId, sections[sectionId].length);
            });
        });
    });
})()
