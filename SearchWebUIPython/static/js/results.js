$(document).ready(function () {
    var url = new URL(window.location.href);
    var id = url.searchParams.get("id");
    var count = url.searchParams.get("c");

    $.getJSON("/get_answers_for_question/" + id, function (data) {

        var items = [];
        $.each(data.a, function (key, val) {
            items.push("                    <div class=\"card-body\" style=\"padding-top: 0;padding-bottom: 0px\">\n" +
                "                        <div class=\"card border-secondary mb-3\" style=\"border:1px solid #dfdfdf !important;border-radius:0;\">\n" +
                "                            <div class=\"card-body text-secondary\">\n" +
                val.body +
                "                            </div>\n" +
                "                        </div>\n" +
                "                    </div>");


        });

        $("<div/>", {
            "id": "content",
            html: items.join("")
        }).appendTo("#answers_content");

        $('#title').html(data.q.title);
        $('#score').html(data.q.score);
        $('#q_body').html(data.q.body);
        $('#count').html(count);



        $('pre code').each(function (i, block) {
            hljs.highlightBlock(block);
        });
    });
});