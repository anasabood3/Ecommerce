$(document).ready(
  function () {
    var csrf = $("input[name=csrfmiddlewaretoken]").val();
    $("#products").on('click', '.add_to_wishlist', function () {
      $.ajax({
        url: $(this).data('url'),
        type: 'post',
        data: {
          product_id: $(this).data('pid'),
          csrfmiddlewaretoken: csrf
        },
        success: function (response) {
          if (response.state == true) {
            $(this).find('i').attr('class','fa fa-heart mr-2');
            $('#wishlist_alerts').html("Added");
          }
          else {
            $(this).find('i').attr('class','fa fa-heart mr-2');
            $('#wishlist_alerts').html("removed");

          }
          $('#wishlist_alerts').removeAttr('hidden');
          $('#wishlist_length').html(response.length_of_wishlist);
        }
      })
    });


    $('#add_to_wishlist').on('click', function () {
        $.ajax({
        url:$("#add_to_wishlist").data('url'),
        type:'post',
        data:{
          product_id: $("#add_to_wishlist").data('pid'),
          csrfmiddlewaretoken: csrf
        },
        success: function(response){
          if (response.state == true){
            $('#wishlist_alerts').html("Added into wishlist");
            $('#add_to_wishlist i').attr('class','fa fa-heart mr-2');
          }
          else{
            $('#wishlist_alerts').html('Removed from wishlist');
            $('#add_to_wishlist i').attr('class','far fa-heart mr-2');
          }
          $('#wishlist_alerts').removeAttr('hidden');
          $('#wishlist_length').html(response.length_of_wishlist);
        }

        })
    
    });

    // $('#rate_input').on('keyup',console.log('Hello/'))
  }
  

  );



  function ViewProductDetails(product_id){
    $.ajax({
      url: "",
      type: 'get',
      data: {
        "product":product_id,
        "action":"quick_view",},
      success: function (response) {
        $("#quickmodal").find("#product_title").text(response.title);
        $("#quickmodal").find("#product_price").text(response.price);
        $("#quickmodal").find("#product_description").text(response.description);
        $("#quickmodal").append("<img src="+response.image+">");
        console.log(response.image);
        $("#quickmodal").modal('show');
      },
      // handle a non-successful response
      error: function (xhr, errmsg, err) {
        alert("Error !!!")
    }
    });
  }

  function RateProduct(rate_value){
    var csrf = $("input[name=csrfmiddlewaretoken]").val();
    $.ajax({
      url: "",
      type: "POST",
      data:{
          rate:rate_value,
          action: "rate",
          csrfmiddlewaretoken: csrf

      },

      // handle a successful response
      success: function (response) {

      },
      // handle a non-successful response
      error: function (xhr, errmsg, err) {
          alert("Error !!!")
      }
  });
  }