$(document).ready(function () {
    $.getJSON("/get_random_questions_from_hbase", function (data) {
        var items = [];
        $.each(data, function (key, val) {
            items.push("<div class=\"card-body\">\n" +
                "                        <div class=\"card border-secondary mb-3\" style=\"border:1px solid #dfdfdf !important;border-radius:0;\">\n" +
                "                            <div class=\"card-header\" style=\"border-bottom-style: dashed;background-color: rgba(0, 0, 0, 0.03)\">\n" +
                "                                <div style=\"margin-right:20px;background-color: #0068b9;border-radius: 5px;padding:7px;\" class=\"float-left\">\n" +
                "                                    <div class=\"text-center\" style=\"font-size: 30px;font-weight: 600;color: #FFFFFF;\">10</div>\n" +
                "                                    <div style=\"color:#FFFFFF\">Answers</div>\n" +
                "                                </div>\n" +
                "                                <div style=\"color:#0078d5;font-weight: bold;margin-left:10px;font-size: 18px; line-height:100%;align-items: center;padding-bottom: 5px\">\n" +
                "                                    <a style=\"color:#0078d5;\" href=\"results.html\">"+val.title+"</a>\n" +
                "                                </div>\n" +
                "                                <div>\n" +
                "                                    <label style=\"font-weight: bold;color:#666666;padding-right: 10px;padding-top:10px\">Score: </label><span>"+val.score+"</span>\n" +
                "                                    <label style=\"font-weight: bold;color:#666666;padding-right: 10px;padding-left:10px\">Date </label><span>"+val.date+"</span>\n" +
                "                                </div>\n" +
                "\n" +
                "                            </div>\n" +
                "                            <div class=\"card-body text-secondary\">\n" +
                                                val.body+
                "                            </div>\n" +
                "                            <div class=\"card-footer text-muted\" style=\"border-top-style: dashed\">\n" +
                "                                <a href=\"#\" style=\"padding:5px\">python</a><a href=\"#\" style=\"padding:5px\">panda</a>\n" +
                "                            </div>\n" +
                "                        </div>\n" +
                "                    </div>");
        });

        $("<div/>", {
            "id": "search-results",
            html: items.join("")
        }).appendTo("#search-container");
    });
});

