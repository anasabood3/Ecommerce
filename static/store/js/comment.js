function create_reply(id) {
    var parent = $("#" + id);
    reply_form = $("#reply_form");
    if (reply_form) {
        reply_form.remove();
    }

    var reply_template = '<form class="row g-3" method="post" id="reply_form">\
    <input type="hidden" name="csrfmiddlewaretoken" value="'+ $("input[name=csrfmiddlewaretoken]").val() + '">\
        <div class="col-auto">\
            <select name="parent" class="d-none" id="id_parent"><option value="'+ id + '" selected="' + id + '"></option></select>\
            <input type="text" name="content" maxlength="255" required="" id="id_content">\
        </div>\
        <div class="col-auto">\
          <button type="submit" class="btn btn-primary mb-3">Reply</button>\
        </div>\
    </form>';

    parent.append(reply_template);

    $("#reply_form").on("submit", function (event) {
        event.preventDefault();
        comment(event);
    });
    
}


function comment(event) {
    const clicked_form = $(event.target);
    var serializedData = clicked_form.serialize();
    // var csrf = $("input[name=csrfmiddlewaretoken]").val();
    $.ajax({
        url: "",
        type: "POST",
        data:serializedData + "&action=comment",

        // handle a successful response
        success: function (response) {
            reply_btn = "";
            var form_template = '<div class="col-lg-8 border border-primary">\
                <div class="media mb-3"><img class="rounded-circle" src="https://www.w3schools.com/howto/img_avatar.png" alt="" width="50">\
                    <div class="media-body ml-3">\
                        <h6 class="mb-0 text-uppercase"> </h6>\
                        <p class="small text-muted mb-0 text-uppercase">Feb. 11, 2022</p>\
                        <p class="text-small mb-0 text-muted" id="'+ response.comment_id + '">' + response.text + '</p>\
                    </div>'+ reply_btn + '\
                </div>\
            </div>';
            if (response.parent != null) {
                reply_btn = '<button class="button" onclick="create_reply(' + response.comment_id + ')">Reply</button>'
                $('#' + response.parent).append(form_template);
            }
            else {
                $('#comments_section').append(form_template);
            }

        },
        // handle a non-successful response
        error: function (xhr, errmsg, err) {
            alert("Error !!!")
        }
    });
}





$("#comment_form").on("submit", function (event) {
    event.preventDefault();
    comment(event);
});

