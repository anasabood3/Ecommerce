function create_reply(id) {

    var parent = $("#" + id);
    reply_form = $("#reply_form");
    if (reply_form) {
        reply_form.remove();
    }

    var reply_template = `<div class="card shadow-sm my-1 bg-light" id="reply_form">
    <div class="card-body">
        <form method='post'>
            <input type="hidden" name="csrfmiddlewaretoken" value="${$("input[name=csrfmiddlewaretoken]").val()}">
            <div class="form-group">
                <select name="parent" class="d-none" id="id_parent"><option value="${id}" selected="${id}"></option></select>\
                <input type="text" name='content' class="form-control form-control-sm" id="id_content" placeholder="Add reply ...">
            </div>
            <button type="submit" class="btn btn-primary btn-sm">Reply</button>
        </form>
    </div>
    </div>`;

    parent.after(reply_template);

    // handle reply form
    $("#reply_form").on("submit", function (event) {
        event.preventDefault();
        comment(event);
        this.remove();
    });

}


function comment(event) {
    const clicked_form = $(event.target);
    var serializedData = clicked_form.serialize();
    $.ajax({
        url: "",
        type: "POST",
        data: serializedData + "&action=comment",

        // handle a successful response
        success: function (response) {


            var reply_template = `<div class="media mb-3 ml-5" id="${response.comment_id}">
                <img class="rounded-circle" src="https://cdn.pixabay.com/photo/2021/02/27/16/25/woman-6055084__340.jpg" alt="" width="50">
                <div class="media-body ml-3">
                <h6 class="text-info text-small mb-0 text-uppercase">${response.commenter}</h6>
                <p class="text-small text-muted mb-0">${response.created}</p>
                <p class="text-small mb-0">${response.text}</p>
                </div>
            </div> `;


            var comment_template = `<div class="media mb-3" id="${response.comment_id}">
                <img class="rounded-circle" src="https://cdn.pixabay.com/photo/2021/02/27/16/25/woman-6055084__340.jpg" alt="" width="50">
                <div class="media-body ml-3">
                <h6 class="text-info text-small mb-0 text-uppercase">${response.commenter}</h6>
                <p class="text-small text-muted mb-0">${response.created}</p>
                <p class="text-small mb-0">${response.text}</p>
                </div>
                <button type="button" onclick="create_reply(${response.comment_id})" class="btn btn-outline-primary btn-sm">Reply</button>
            </div> `;


            // if this is a reply
            if (response.parent != null) {
                $('#' + response.parent).after(reply_template);
            }
            // if this is regulare comment
            else {
                $('#comments_section').prepend(comment_template);
            }

        },
        // handle a non-successful response
        error: function (xhr, errmsg, err) {
            alert("Error:" + err)
        }
    });
}




// hander regulare comment form
$("#comment_form").on("submit", function (event) {
    event.preventDefault();
    comment(event);
    this.reset();
});





