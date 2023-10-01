$(document).ready(function(){
    $('.add-the-cart').on('click' , function(e){
        e.preventDefault();
        food_id = $(this).attr('data-id');
        url= $(this).attr('data-url');
        $.ajax({
            type : "GET",
            url : url,
            success : function(response){
                console.log(response);
                if (response.status == 'login_required') {
                    Swal.fire({
                        text:  response.message ,
                        icon: 'info',
                        confirmButtonColor: '#3085d6',
                        confirmButtonText: 'OK'
                      }).then(function(){
                        window.location = '/login';
                      });
                }
                if(response.status == 'failed'){
                    Swal.fire({
                        text:  response.message ,
                        icon: 'error',
                        confirmButtonColor: '#3085d6',
                        confirmButtonText: 'OK'
                      })
                }
                else {
                    //decrease live cart count to template 
                    $('#cart-counter').html(response.cart_counter['cart_count']);
                    $('#qty-'+food_id).html(response.qty);

                    //subtotal tax total price 
                    CartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['total'],
                    )
                }
            }
        });
    })

    $('.item_qty').each(function(){
        var the_id = $(this).attr('id')
        var qty = $(this).attr('data-qty')
        $('#'+the_id).html(qty)
    })

    
    $('.decrease-the-cart').on('click' , function(e){
        e.preventDefault();
        food_id = $(this).attr('data-id');
        url= $(this).attr('data-url');
        cart_id = $(this).attr('id');
        $.ajax({
            type : "GET",
            url : url,
            success : function(response){
                console.log(response);
                if (response.status == 'login_required') {
                    Swal.fire({
                        text:  response.message ,
                        icon: 'info',
                        confirmButtonColor: '#3085d6',
                        confirmButtonText: 'OK'
                      }).then(function(){
                        window.location = '/login';
                      });
                }
                if(response.status == 'failed'){
                    Swal.fire({
                        text:  response.message ,
                        icon: 'error',
                        confirmButtonColor: '#3085d6',
                        confirmButtonText: 'OK'
                      })
                }
                else {
                    //decrease live cart count to template 
                    $('#cart-counter').html(response.cart_counter['cart_count']);
                    $('#qty-'+food_id).html(response.qty);
                    // run only in cart page 
                    if(window.location.pathname == '/cart/'){
                        removecartitem(response.qty , cart_id );
                        CheckEmptyCart();
                        CartAmounts(
                            response.cart_amount['subtotal'],
                            response.cart_amount['tax'],
                            response.cart_amount['total'],
                        )
                    }
                }
            }
        });
        
    });

    $('.delete-cart').on('click' , function(e){
        e.preventDefault();
        cart_id = $(this).attr('data-id');
        url= $(this).attr('data-url');
        $.ajax({
            type : "GET",
            url : url,
            success : function(response){
                console.log(response);
                if(response.status == 'failed'){
                    Swal.fire({
                        text:  response.message ,
                        icon: 'error',
                        confirmButtonColor: '#3085d6',
                        confirmButtonText: 'OK'
                      })
                }
                else {
                    //decrease live cart count to template 
                    $('#cart-counter').html(response.cart_counter['cart_count']);
                    swal.fire(response.status , response.message , 'success');

                    removecartitem(0 , cart_id)
                    CartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['total'],
                    )
                }
            }
        });
    })
    // remove li tag  cartitem when call 
    function removecartitem(cartitemqty , card_id){
        // first  check the path  and run this code 
        if(window.location.pathname == '/cart/'){
            if (cartitemqty <=0){
                //remove the item elemnt 
                document.getElementById("cart-item-"+cart_id).remove()
                CheckEmptyCart()
            }
        }
    }
    // check empty card by read the cart-counter 
    function CheckEmptyCart(){
        var Cart_counter = document.getElementById('cart-counter').innerHTML;
        if (Cart_counter == 0 ){
            var get_element = document.getElementById('empty-cart');
            get_element.style.display = 'block' ;
        }
    
    }

    // cart amounts 

    function CartAmounts(subtotal , tax , total){
        if(window.location.pathname == '/cart/'){
            $('#subtotal').html(subtotal)
            $('#tax').html(tax)
            $('#total').html(total)
        }
    }
    
});