(function() {
    function getThreads(sectionId, offset) {
        $.get("/sections/" + sectionId + "/threads?limit=5&offset=" + offset)
            .done(function(threads) {
                    addThreads(sectionId, threads);
                }
            )
    }


    var sections = {};

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
            var dom = $("<div class='p-2 m-2 border bg-white'><a href='/thread/" + thread.id + "'>" + thread.title + "</a><br><p class='text-right'>Created by: " + thread.author + "</p></div>");
            container.append(dom);
        }
    }

    function test() {

    }

    $(function() {
        test();
        $("a[data-toggle='tab']").each(function() {
            var sectionId = this.attributes["data-section-id"].value;
            var jq = $(this);
            $("#new_thread").click(function() {
                alert("test");
            });
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
