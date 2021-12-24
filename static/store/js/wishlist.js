$(document).ready(
    
    function () {
       
        var csrf = $("input[name=csrfmiddlewaretoken]").val();
        $("#products_list").on('click', '.remove_product', function () {
            $.ajax({
                url: $(this).data('url'),
                type: 'post',
                data: {
                    product_id: $(this).data('pid'),
                    csrfmiddlewaretoken: csrf
                },
                success: function (response) {

                    $(this).hide();
                    // $('#wishlist_alerts').html("removed");
                    // $('#wishlist_alerts').removeAttr('hidden');
                    $('#wishlist_length').html(response.length_of_wishlist);
                }
            })
        });



    });