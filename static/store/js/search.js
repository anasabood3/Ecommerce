$(document).on('keyup', '#id_q', function (e) {
    e.preventDefault();

    var minlength = 3;
    var results = [];

    if ($('#id_q').val().length >= minlength) {
        $.ajax({
            type: 'POST',
            url: '/search/',
            data: {
                ss: $('#id_q').val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                action: 'post'
            },
            success: function (json) {

                $.each(JSON.parse(json.search_string), function (i, item) {

                    results.push('<li class="my-2 pl-2"><a href="/products/'+item.fields.slug+'">' + item.fields.title +'</a></li>')
                   
                })

                if (!$(".show")[0]) {
                    $('.menudd').trigger('click')
                }

                document.getElementById("list").innerHTML = (!results.length) ?
                    "No results match your query" : results.join('');
            },
            error: function (xhr, errmsg, err) {}
        });
    }
});