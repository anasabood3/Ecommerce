const csrf = $("input[name=csrfmiddlewaretoken]").val();



$(document).ready(
  function () {

    $("#products").on('click', '.add_to_wishlist', function () {
      btn = $(this).data('pid');
      obj = $(this).find('i');
      AddtoWishList(btn, obj, _response);

    });


    $('#add_to_wishlist').on('click', function () {
      obj = $(this).find('i');
      AddtoWishList($(this).data('pid'), obj, _response);

    });

    $('#products_list').on('click', '.remove_product', function () {
      obj = $(this).closest('tr');
      AddtoWishList($(this).data('pid'), obj, whishlist_response);

    });

  }
);

function AddtoWishList(product_slug, obj, callback) {
  $.ajax({
    url: `/products/${product_slug}`,
    type: 'post',
    data: {
      product_id: product_slug,
      "action": "add_to_whishlist",
      csrfmiddlewaretoken: csrf,
    },
    success: (response) => {
      callback(response, obj);
    },
    error: (xhr, errmsg, err) => {
      alert(err);
    }
  });
}

function _response(response, obj) {
  if (response.state == true) {

    obj.attr('class', 'fa fa-heart');
  }
  else {

    obj.attr('class', 'far fa-heart');

  }

  $('#wishlist_length').html(response.length_of_wishlist);
}


function whishlist_response(response, obj) {

  $('#wishlist_length').html(response.length_of_wishlist);
  $('#wl-count span').html(response.length_of_wishlist + ' items');

  let total_element = $('#wl-total span');
  let old_amount = parseInt(total_element.html());

  let new_amount = old_amount - response.decrease_amount;
  $('#wl-total span').html(new_amount);
  obj.remove();
}

function ViewProductDetails(product_id) {
  $.ajax({
    url: "",
    type: 'get',
    data: {
      "product": product_id,
      "action": "quick_view",
    },
    success: function (response) {
      $("#quickmodal").find("#product_title").text(response.title);
      $("#quickmodal").find("#product_price").text(response.price);
      $("#quickmodal").find("#product_description").text(response.description);
      $("#quickmodal").append("<img src=" + response.image + ">");
      $("#quickmodal").modal('show');
    },
    // handle a non-successful response
    error: function (xhr, errmsg, err) {
      alert("Error:"+err);
    }
  });
}

function RateProduct(rate_value) {
  var csrf = $("input[name=csrfmiddlewaretoken]").val();
  $.ajax({
    url: "",
    type: "POST",
    data: {
      rate: rate_value,
      action: "rate",
      csrfmiddlewaretoken: csrf

    },
    success: function (response) {

    },
    error: function (xhr, errmsg, err) {
      alert("Error:" + err)
    }
  });
}


