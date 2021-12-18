$(document).ready(function () {
var csrf = $("input[name=csrfmiddlewaretoken]").val();
  $("#deleteAccount").on('click',function(){
  $.ajax({
  url:$("#deleteAccount").data('url'),
  type:'post',
  data:{
      confirm_delete:$("#accountDeleteConfirm").is(":checked"),
      csrfmiddlewaretoken: csrf
  },
  success: function(response){
    if (response.state == true)
    {
        window.location.reload();
    }
    else{
    $("#deleteError").text(response.error);
    $("#deleteError").removeAttr('hidden');
    }

  }

  })
  });

});
