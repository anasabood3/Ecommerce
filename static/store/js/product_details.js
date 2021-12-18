$(document).ready(function () {
var csrf = $("input[name=csrfmiddlewaretoken]").val();
  $("#add_to_wishlist").on('click',function(){

  $.ajax({
  url:$("#add_to_wishlist").data('url'),
  type:'post',
  data:{
    product_id: $("#add_to_wishlist").data('pid'),
    csrfmiddlewaretoken: csrf
  },
  success: function(response){
    $('#wishlist_length').text(response.wishlist_items)
  }

  })
  });

});