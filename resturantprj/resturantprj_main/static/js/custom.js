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
                        response.cart_amount['tax_dict'],
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
                            response.cart_amount['tax_dict'],
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
                        response.cart_amount['tax_dict'],
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

    function CartAmounts(subtotal , tax_dict , total){
        if(window.location.pathname == '/cart/'){
            $('#subtotal').html(subtotal)
            $('#total').html(total)
            // get tax amount 
            for(key in tax_dict){
                //set value precentage as key and return tax amout  
                for(value1 in tax_dict[key]){
                    $('#tax-'+key).html(tax_dict[key][value1])

                }
            }
        }
    }
    

    //add hour in opening hours

    $('.add_hour').on('click' , function(e){
        e.preventDefault();
        var day = document.getElementById('id_day').value;
        var for_hour = document.getElementById('id_from_hour').value;
        var to_hour = document.getElementById('id_to_hour').value;
        var is_closed = document.getElementById('id_is_closed').checked ;//return true or false
        var csrf_token = $('input[name=csrfmiddlewaretoken]').val();
        var url = document.getElementById('add_url').value;


        if(is_closed){
            is_closed = 'True' ; // true in python is True
            condition= "day != ''" ;
        }else{
            is_closed = 'False';
            condition = "day != '' && for_hour != '' && to_hour != '' "
        }


        if(eval(condition) ){
            $.ajax({
                type : 'POST',
                url : url , 
                data : {
                    'day' : day,
                    'from_hour':for_hour,
                    'to_hour' : to_hour,
                    'is_closed' : is_closed,
                    'csrfmiddlewaretoken':csrf_token,
                },
                success : function(response){
                    if (response.status == 'success'){
                        if(response.is_closed == 'Closed'){
                            html = '<tr id="hour-'+response.id+'"><td><b>'+ response.day +'</b></td><td>'+ 'Closed' +'</td><td><a href="#" class="remove_hour" data-url="/vendor/opening_hours/remove/'+response.id+'/">Remove</a></td></tr>' 
                        }
                        else{
                            html = '<tr id="hour-'+response.id+'"><td><b>'+ response.day +'</b></td><td>'+response.from_hour +'-'+response.to_hour+'</td><td><a href="#" class="remove_hour" data-url="/vendor/opening_hours/remove/'+response.id+'/">Remove</a></td></tr>'
                        }
                        $('.opening_hours').append(html)
                        document.getElementById("form_hour").reset()
                    }
                    else{
                        swal.fire(response.message , '', 'error')
                    }
                }
            })
        }else{
            Swal.fire("fill all inputs" , '' , 'info')
        }

    })
    
    //delete the hour in opening hours 
    $(document).on('click', '.remove_hour', function(e) {
        e.preventDefault();
        var url = $(this).attr('data-url');
        var rowId = $(this).closest('tr').attr('id');
        $.ajax({
            type: 'GET',
            url: url,
            success: function(response) {
                if (response.status == "success") {
                    $('#' + rowId).remove();
                }
            }
        });
    });
});