function AddtoWishList(product_slug,callback){
    $.ajax({
      url:`/products/${product_slug}`,
      type:'post',
      data:{
        product_id: product_slug,
        "action":"add_to_whishlist",
        csrfmiddlewaretoken: csrf,
      },
      success: (response)=>{
        callback(response);
      },
      error:(xhr,errmsg,err)=>{
            alert(err);
      }
  });
  }
