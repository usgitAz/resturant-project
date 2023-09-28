let autocomplete;

function initAutoComplete(){
autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address'),
    {
        types: ['geocode', 'establishment'],
        //default in this app is "IN" - add your country code
        componentRestrictions: {'country': ['in']},
    })
// function to specify what should happen when the prediction is clicked
autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged (){
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry){
        document.getElementById('id_address').placeholder = "Start typing...";
    }
    else{
        console.log('place name=>', place.name)
    }
    // get the address components and assign them to the fields
}

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
                }
            }
        });
    })


    
});