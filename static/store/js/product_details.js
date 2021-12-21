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
    if (response.state == true){
      $('#wishlist_alerts').html("Added into wishlist");
      $('#add_to_wishlist span').html('Remove from wishlist');
    }
    else{
      $('#wishlist_alerts').html('Removed from wishlist');
      $('#add_to_wishlist span').html('Add into wishlist');
    }
    $('#wishlist_alerts').removeAttr('hidden');
    $('#wishlist_length').text(response.wishlist_items);
  }

  })
  });

});