$(document).ready(function () {
    "use strict";

    PageScroll();




    // Loading Box (Preloader)
    function handlePreloader() {
        if ($('.preloader').length > 0) {
            $('.preloader').delay(200).fadeOut(500);
        }
    }

    handlePreloader();

    $('.minus').click(function () {
        var $input = $(this).parent().find('input');
        var count = parseInt($input.val()) - 1;
        count = count < 1 ? 1 : count;
        $input.val(count);
        $input.change();
        return false;
    });
    $('.plus').click(function () {
        var $input = $(this).parent().find('input');
        $input.val(parseInt($input.val()) + 1);
        $input.change();
        return false;
    });

    // OWL SLIDER
    $('.category-slider').owlCarousel({
        loop: true,
        margin: 4,
        nav: true,
        autoplay: false,
        dots: false,
        navText: ['<i class="feather-arrow-left-circle"></i>', '<i class="feather-arrow-right-circle"></i>'],
        autoWidth: true
    })

    $('.slider-banner').owlCarousel({
        loop: false,
        margin: 10,
        nav: true,
        autoplay: false,
        dots: true,
        navText: ['<i class="feather-chevron-left"></i>', '<i class="feather-chevron-right"></i>'],
        items: 1,
    })
    $('.product-banner').owlCarousel({
        loop: false,
        margin: 0,
        nav: true,
        autoplay: false,
        dots: true,
        navText: ['<i class="feather-chevron-left"></i>', '<i class="feather-chevron-right"></i>'],
        items: 1,
    })
    $('.slider-banner-2').owlCarousel({
        loop: false,
        margin: 10,
        nav: true,
        autoplay: false,
        dots: false,
        navText: ['<i class="feather-chevron-left"></i>', '<i class="feather-chevron-right"></i>'],
        autoWidth: true
    })

    $('.slider-banner-3').owlCarousel({
        loop: true,
        margin: 10,
        nav: true,
        autoplay: false,
        dots: true,
        navText: ['<i class="feather-chevron-left"></i>', '<i class="feather-chevron-right"></i>'],
        items: 3,
        center: true,
    })

    $('.banner-slider-3').owlCarousel({
        loop: true,
        margin: 0,
        nav: true,
        autoplay: false,
        dots: false,
        navText: ['<i class="feather-arrow-left-circle"></i>', '<i class="feather-arrow-right-circle"></i>'],
        items: 3,
        responsive: {
            0: {
                items: 1,
                nav: true
            },
            749: {
                items: 3,
                nav: true
            }
        }
    })

    $('.banner-slider-4').owlCarousel({
        loop: true,
        margin: 0,
        nav: true,
        autoplay: false,
        dots: false,
        navText: ['<i class="feather-arrow-left-circle"></i>', '<i class="feather-arrow-right-circle"></i>'],
        items: 4,
        responsive: {
            0: {
                items: 2,
                nav: true
            },
            749: {
                items: 4,
                nav: true
            }
        }
    })

    $('.banner-slider-5').owlCarousel({
        loop: true,
        margin: 0,
        nav: true,
        autoplay: false,
        dots: false,
        navText: ['<i class="feather-arrow-left-circle"></i>', '<i class="feather-arrow-right-circle"></i>'],
        items: 5,
        responsive: {
            0: {
                items: 2,
                nav: true
            },
            749: {
                items: 4,
                nav: true
            },
            1023: {
                items: 5,
                nav: true
            }
        }
    })



    $(".nav-item-toggle").on({
        mouseenter: function () {
            $(this).children().addClass('show');
        },
        mouseleave: function () {
            $(this).children().removeClass('show');
        }
    });

    $('.toggle-nav').on('click', function () {
        $('.navigation,.main-content,.nav-header').toggleClass('menu-active');
        return false;
    });
    $('.wishlist-btn').on('click', function () {
        $(this).find('i').toggleClass('text-grey-500 text-success');
        return false;
    });

    $('.category-card').on('click', function () {
        $('.category-card').removeClass('active');
        $(this).addClass('active');
        return false;
    });


    // navigation slide menu mobile
    $('.nav-menu').on('click', function () {
        $(this).toggleClass('active');
        $('.navigation').toggleClass('nav-active');
    });
    $('.close-nav').on('click', function () {
        $('.navigation').removeClass('nav-active');
        return false;
    });
    $('.nav-link').on('click', function () {
        $('.nav-link').removeClass('active');
        $(this).addClass('active');
        return false;
    });


    $('input[name="color-radio"]').on('change', function () {
        if (this.checked) {
            $('body').removeClass('color-theme-teal color-theme-cadetblue color-theme-pink color-theme-deepblue color-theme-blue color-theme-red color-theme-black color-theme-gray color-theme-orange color-theme-yellow color-theme-green color-theme-white color-theme-brown color-theme-darkgreen color-theme-deeppink color-theme-darkorchid');
            $('body').addClass('color-theme-' + $(this).val());
        }
    });




    $('#checkout').on('click', function () {
        $('.cart-box').fadeOut(0);
        $('.checkout-box').fadeIn();
    });
    $('#payment').on('click', function () {
        $('.checkout-box').fadeOut(0);
        $('.payment-box').fadeIn();
    });

    $(window).on('load', function () {
        $('#modalSubscribe').modal('show');
    });

});


function PageScroll() {
    $(".scroll-tiger").on("click", function (e) {
        var $anchor = $(this);
        $("html, body").stop().animate({
            scrollTop: $($anchor.attr("href")).offset().top - 0
        }, 1500, 'easeInOutExpo');
        $('.overlay-section').removeClass('active');
        e.preventDefault();

    });
}

function searchLocationClick(index) {

    var add = document.getElementById("p-tag-" + index).innerHTML;

    document.getElementById("user_input_autocomplete_address").value = jQuery.trim(add).substring(0, 40);
    $('#location-list').empty();
    $('#location-list').hide();
    $('.success-loction').show();
    $('.error-loction').hide();
}

jQuery(document).ready(function () {
    $('.address-save-btn').click(function (e) {
        e.preventDefault();

        address = document.getElementById("user_input_autocomplete_address").value;
        console.log("calling ");
        domain = window.location.origin
        console.log(domain);
        path_name = '/accounts/user-address/' //change-this url
        $.ajax({
            type: 'POST',
            url: domain + path_name,
            data: {
                "csrfmiddlewaretoken": g_csrftoken,
                "address": address
            },
            success: function (response) {
                if (response) {
                    console.log(response);
                }
            }
        })
    });
});


function showLocationSearch(value) {
    console.log(value);
    domain = window.location.origin
    path_name = '/stores/suggest-delivery-location/' //change-this url
    if (value.length < 5) {
        $('#location-list').empty()
        $('#location-list').hide()
        $('.error-loction').hide();
        $('.success-loction').hide();
    }
    else {
        $.ajax({
            type: 'GET',
            url: domain + path_name,
            contentType: 'application/json',
            data: {
                "csrfmiddlewaretoken": g_csrftoken,
                "value": value,

            },
            statusCode: {
                404: function (responseObject, textStatus, jqXHR) {
                    $('.success-loction').hide();
                    $('.error-loction').show();
                    $('#location-list').empty();
                    $('#location-list').hide();
                    $("#save-button-address").attr("disabled", true);
                    $("#save-button-address").css({ "background-color": "#ccc", "transition": "0.3s" });
                }
            },
            success: function (response) {
                if (response) {
                    console.log(response);
                    $('.error-loction').hide();
                    $("#save-button-address").attr("disabled", false);
                    $("#save-button-address").css({ "background-color": "green", "transition": "0.3s" });
                    $('#location-list').empty()
                    sessionStorage.setItem('response', response);

                    console.log(response);
                    $('#location-list').show()
                    $.each(response, function (index, item) {
                        var res = JSON.stringify(item)
                        $('#location-list').append(`
                          <div class="suggest-location d-flex col-12 cstm-area" >
                            <div class="location_name col-8 align-self-center" id="`+ index + `" onclick="searchLocationClick(this.id)">
                              <p id="p-tag-`+ index + `">` + item.area + `,` + item.sector + `,` + item.city + `,` + item.pincode + `</p>
                            </div>
                          </div>
                        `)
                    })
                }

            }

        });
    }

}




jQuery(document).ready(function () {
    $('.plus-bttn').click(function (e) {
        e.preventDefault();
        const elementId = $(this).attr('id').split('-')[0]
        const cate = $(this).attr('id').split(":")[1]
        domain = window.location.origin
        path_name = '/buy/customer/order/add/' //change-this url
        $.ajax({
            type: 'POST',
            url: domain + path_name,
            data: {
                "csrfmiddlewaretoken": g_csrftoken,
                "product": elementId.toString(),
                "quantity": "1"
            },
            success: function (response) {
                if (response) {
                    console.log(response);
                    document.getElementById("cart-amount").innerHTML = "₹" + response['amount'];
                    document.getElementById("quantity").innerHTML = response['qty'];
                    document.getElementById(elementId + "-qunt_val-" + cate).innerHTML = response['item_qty'];
                }
            }
        })
    });

    $('.posasf').click(function (e) {
        e.preventDefault();
        const elementId = $(this).attr('id').split('-')[0]
        const cate = $(this).attr('id').split(":")[1]
        domain = window.location.origin
        path_name = '/buy/customer/order/add/' //change-this url
        $.ajax({
            type: 'POST',
            url: domain + path_name,
            data: {
                "csrfmiddlewaretoken": g_csrftoken,
                "product": elementId.toString(),
                "quantity": "1"
            },
            success: function (response) {
                if (response) {
                    document.getElementById("cart-amount").innerHTML = "₹" + response['amount'];
                    document.getElementById("quantity").innerHTML = response['qty'];
                    document.getElementById(elementId + "-qunt_val-" + cate).innerHTML = response['item_qty'];
                }
            }
        })
    });

    $('.minus-bttn').click(function (e) {
        e.preventDefault();
        const elementId = $(this).attr('id').split('-')[0]
        const cate = $(this).attr('id').split(":")[1]
        domain = window.location.origin
        path_name = '/buy/customer/order/remove/' //change-this url
        $.ajax({
            type: 'POST',
            url: domain + path_name,
            data: {
                "csrfmiddlewaretoken": g_csrftoken,
                "product": elementId.toString(),
                "quantity": "1"
            },
            success: function (response) {
                if (response) {
                    document.getElementById("cart-amount").innerHTML = "₹" + response['amount'];
                    document.getElementById("quantity").innerHTML = response['qty'];
                    document.getElementById(elementId + "-qunt_val-" + cate).innerHTML = response['item_qty'];
                    if (response['item_qty'] == 0) {
                        $("#" + elementId + "-in-dec-" + cate).hide();
                        $('.b-' + cate + '-' + elementId).show();
                    }
                }
            }
        })
    });
});

function hidePopLogin() {
    $('#login').hide()
    $('body').css({ "overflow": "auto" })
}

function showPopLogin() {
    history.scrollRestoration = "manual";
    scrollToTop(0);
    $('#login').show()
    $('body').css({ "overflow": "hidden" })
}

function showPopsearch(em_id) {
    $('#' + em_id).show()
    $('body').css({ "overflow": "hidden" })
}

function scrollToTop(hei) {
    window.scrollTo({
        top: hei,
        left: 0,
        behavior: 'smooth'
    });
}


window.onscroll = function () {
    if (document.body.offsetWidth < 500) {
        if (window.pageYOffset > 70) {
            $('.top_location .dev_time_text').hide()
            $('.top_location form').css({ "margin-top": "20px", "transition": "0.3s" })
        }
        else if (window.pageYOffset < 70) {
            $('.top_location .dev_time_text').show()
            $('.top_location form').show().css({ "margin-top": "0px", "transition": "0.3s" })
        }
    }
}

function showLoader() {
    $('body').append('<div style="" id="loadingDiv"><div class="loader"><img src=""></div></div>');
}

function hideLoader() {
    $('.loader').hide();
}

function showLocation(position) {
    var lat = position.coords.latitude;
    var long = position.coords.longitude;
    document.getElementById("user_input_autocomplete_address").disabled = true;
    document.getElementById("current-location").value = "Please Wait...";

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var address = JSON.parse(this.responseText)
            var comp = address.results[0].address_components;
            //console.log(comp[comp.length - 1].long_name); print( zipcode)
            var zipcode = comp[comp.length - 1].long_name;
            sessionStorage.setItem("pincode", zipcode);
            checkStoreAvailabilty(address.results[0].formatted_address);
            /* var pincode = sessionStorage.getItem("pincode");
            console.log(pincode); 
            */
            // Save zipcode to sessionStorage

            document.cookie = 'pincode=' + zipcode + ";domain=;path=/";
            document.cookie = 'address=' + address.results[0].formatted_address + ";domain=;path=/";

            document.getElementById("current-location").value = "Use My Current Location";
            document.getElementById("user_input_autocomplete_address").disabled = false;
            document.getElementById("user_input_autocomplete_address").value = address.results[0].formatted_address;
            $('#location-text').empty()
            $('#location-text').text(String(address.results[0].formatted_address).slice(0, 35) + '... ')
            $('#location-text').append(`<i class="bi bi-caret-down-fill"></i>`)

            sessionStorage.setItem("Address", address.results[0].formatted_address);
        }
    };
    xhttp.open("GET", "https://maps.googleapis.com/maps/api/geocode/json?latlng=" + lat + "," + long + "&key=AIzaSyBYSvhqF-DYy0C78aP35lME_p7esEqCbCo", true);
    xhttp.send();
    // alert("Latitude : " + latitude + " Longitude: " + longitude);
};

var getCookie = function (name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

const g_csrftoken = getCookie('csrftoken');

function showProducts(value) {

    console.log(value)
    domain = window.location.origin
    path_name = '/stores/products/' //change-this url
    if (value.length < 3) {
        $('.suggestProduct').empty()
        $('.suggestProduct').hide()
    }
    else {
        $.ajax({
            type: 'GET',
            url: domain + path_name,
            data: {
                "csrfmiddlewaretoken": g_csrftoken,
                "products": value,

            },
            success: function (response) {
                if (response) {
                    //console.log(response)
                    $('.suggestProduct').empty()

                    if (response.length > 0) {
                        $('.suggestProduct').show()
                        $.each(response, function (index, item) {
                            //console.log(response[index].products.product_id)
                            $('.suggestProduct').append(`
                          <div class="suggest-product d-flex col-12" onclick='window.location.href="/productdetail/`+ response[index].products.product_id + `"' >
                            <div class="col-2 ">
                              <img src="`+ response[index].products.prod_mainimage + `" alt=""  >
                            </div>
                            <div class="product_name col-8 align-self-center">
                              <p>`+ response[index].products.product_name + `</p>
                            </div>
                            <div class="align-self-center">
                              <div class="product_pirce "><span class="pro_mrp">`+ response[index].products.max_retail_price + `</span><span class="pro_sell">` + response[index].products.max_retail_price + `</span></div>
                              <!-- <a href="#" class="btn btn-style1 btn-padding">ADD</a> -->
                            </div>
                          </div>
                          `)
                        })
                    }
                }
                else {
                    $('.suggestProduct').empty()
                    $('.suggestProduct').show()
                    $('.suggestProduct').append(`
                      <p style="color: red;">Sorry! we regret but we don't have that product, that you search for.</p>
                      `)
                }
            }

        });
    }
}
var checkStoreAvailabilty = function (Fformatted_address) {
    var availablility = null;
    domain = window.location.origin
    path_name = '/stores/availability/'
    $.ajax({
        type: 'GET',
        url: domain + path_name,
        data: {
            "csrfmiddlewaretoken": g_csrftoken,
            "pincode": sessionStorage.getItem('pincode')
        },
        success: function (response) {
            if (response['available']) {
                //console.log(response['available'])
                $('#success-loc').show()
                $('#error-loc').hide()
                //document.getElementById("location-text").innerHTML = Fformatted_address;
                //console.log(Fformatted_address);
                document.getElementById("location-text").innerHTML = jQuery.trim(Fformatted_address).substring(0, 40).split(" ").slice(0, -1).join(" ") + "...";
            }
            else {
                $('#success-loc').hide()
                $('#error-loc').show()
            }
        }
    });

}

//console.log(status)

function errorHandler(err) {
    if (err.code == 1) {
        alert("Error: Access is denied!");
    } else if (err.code == 2) {
        alert("Error: Position is unavailable!");
    }
}
//locationDetect();
function ok_address(id_address) {
    if (id_address.length > 0) {
        document.getElementById("user_input_autocomplete_address").value
        $('#location-text').empty()
        $('#location-text').text(String(document.getElementById("user_input_autocomplete_address").value).slice(0, 35) + '... ')
        $('#location-text').append(`<i class="bi bi-caret-down-fill"></i>`)
        $('#search-popup').hide()
        $('body').css({ "overflow": "auto" })
    }
    else {
        $('#' + id_address).focus()
    }
}
function locationDetect() {

    if (navigator.geolocation) {

        // timeout at 60000 milliseconds (60 seconds)
        var options = {
            timeout: 60000
        };
        navigator.geolocation.getCurrentPosition(showLocation, errorHandler, options);
    } else {
        alert("Sorry, browser does not support geolocation!");
    }
}

function initializeAutocomplete(id) {
    var element = document.getElementById(id);
    if (element) {
        var autocomplete = new google.maps.places.Autocomplete(element, {
            types: ['geocode']
        });
        google.maps.event.addListener(autocomplete, 'place_changed', onPlaceChanged);
    }
}

function onPlaceChanged() {
    var place = this.getPlace();

    // console.log(place);  // Uncomment this line to view the full object returned by Google API.

    for (var i in place.address_components) {
        var component = place.address_components[i];
        for (var j in component.types) { // Some types are ["country", "political"]
            var type_element = document.getElementById(component.types[j]);
            if (type_element) {
                type_element.value = component.long_name;
            }
        }
    }
}

// google.maps.event.addDomListener(window, 'load', function () {
//     initializeAutocomplete('user_input_autocomplete_address');
// }); 

function get_otp(elm) {
    const input = $('#' + elm).val();
    const domain = window.location.origin;
    const path_name = '/accounts/register/get_otp/';
    
    $('#error_login').empty();
    $('#button_submit').attr('disabled', true); // Disable the button while processing the request

    $.ajax({
        type: 'POST',
        url: domain + path_name,
        data: {
            "csrfmiddlewaretoken": g_csrftoken,
            "country_code": "+91",
            "phone_number": input,
            "fake_otp": "True",
            "otp": "123456",
        },
        success: function (response) {
            if (response['Status'] == "Sent") {
                $('#' + elm).hide();
                $("#hide-num-text").hide();
                $("#hide-91").hide();
                $("#mobile").hide();
                $('#button_submit').hide();
                $("#hide-otp-text").show();
                $("#otp").show();
                $("#button_otp").show();
            } else {
                // Handle the case where OTP sending limit is exceeded
                $("#hide-num-text").hide();
                $("#hide-91").hide();
                $("#mobile").hide();
                $('#button_submit').hide();
                $("#hide-otp-text").show();
                $("#otp").show();
                $("#button_otp").show();
                $('#error_login').css("color", "red").text("Limit exceeded").show();
            }
        },
        error: function () {
            // Handle AJAX error, show input fields again
            $("#hide-num-text").show();
            $("#hide-91").show();
            $("#mobile").show();
            $('#button_submit').show();
            $("#hide-otp-text").hide();
            $("#otp").hide();
            $("#button_otp").hide();
        }
    });
}
function verify_otp(input_id) {
    const input = $('#' + input_id).val();
    const phone_number = $('#phone_number').val();
    if (input.length === 6) {
        $('#error_otp').hide();
        const domain = window.location.origin;
        const path_name = '/accounts/register/verify/';

        $.ajax({
            type: 'POST',
            url: domain + path_name,
            data: {
                "csrfmiddlewaretoken": g_csrftoken,
                "country_code": "+91",
                "otp": input,
                "phone_number": phone_number,
                "web": "True",
            },
            success: function (response) {
                if (response) {
                    $('#error_login').empty();
                    $('#error_login').hide();
                    
                    // Show the "Verify" button and hide the OTP input field
                    $("#verifyButtonWrapper").show();
                    $("#otpInputWrapper").hide();
                } else {
                    // Handle the case where OTP verification failed
                    $('#error_login').show().text('Error'); // Change this to handle backend response error.
                }
            }
        });
    } else if (input.length === 0) {
        $('#error_otp').css("color", "red").text("Enter OTP");
    } else {
        $('#error_otp').css("color", "red").text("Invalid OTP Length");
    }
}


function hidePopsearch(em_id) {
    $('#' + em_id).hide()
    $('body').css({ "overflow": "auto" })
}

function showGreenButton(butn, el, len) {
    value = $(el).val()
    if (value.length == len) {
        $('#' + butn).removeAttr("disabled")
        $('#' + butn).attr("type", "submit")
        $('#' + butn).css({ "background-color": "green", "transition": "0.3s" })
    }
    else {
        $('#' + butn).css({ "background-color": "#ccc", "transition": "0.3s" })
        $('#' + butn).attr("disabled")
        $('#' + butn).attr("type", "button")
    }
}

function showPopsearch(em_id) {
    $('#' + em_id).show()
    valu = $('#location-text').text()
    $('#user_input_autocomplete_address').val(valu)
    $('body').css({ "overflow": "hidden" })
}

function showProductDetails(productId) {
    domain = window.location.origin;
    path = '/details/id=';
    $.ajax({
        url: domain + path + productId,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            console.log(data);
            $('#productDetails').html(data.product_html);
            $('#productmodal').modal('show');
        },
        error: function () {
            alert('Error retrieving product details.');
        }
    });
}


$(document).ready(function () {
    $('.list-group-item').click(function (event) {
        event.preventDefault();
        var categoryId = $(this).data('category-id');
        console.log(categoryId);
        $.ajax({
            url: '{% url "filter_by_category" 0 %}'.replace('0', categoryId),
            success: function (data) {
                var productsList = $('#products-list');
                productsList.empty();
                for (var i = 0; i < data.products.length; i++) {
                    var product = data.products[i];
                    var card = $('<div class="owl-items">\
                            <div class="col-lg-12 p-3 rounded-0 posr">\
                                <h4 class="ls-3 font-xsssss text-white text-uppercase bg-current fw-700 p-2 d-inline-block posa rounded-3">'+ product.discount + '% off</h4>\
                                <a href="#" class="posa right-0 top-0 mt-3 me-3"><i class="ti-heart font-xs text-grey-500"></i></a>\
                                <div class="clearfix"></div>\
                                <a class="d-block text-center p-2" onclick="showProductDetails({{dp.id}})">\
                                    <img src="/media/'+ product.image + '" alt="product-image"  class="w-100 mt-1 d-inline-block" height="171px" width="148px">\
                                </a>\
                                <div class="star d-inline text-left">\
                                    {% for i in 1|range:5 %}\
                                        {% if i <= dp.average_rating %}\
                                            <img src="{% static "images/star.png" %}" alt="star" class="w-12 me-1 float-start">\
                                        {% else %}\
                                            <img src="{% static "images/star-disable.png" %}" alt="star" class="w-12 me-2 float-start">\
                                        {% endif %}\
                                    {% endfor %}\
                                </div>\
                                <div class="clearfix"></div>\
                                <h2 class="mt-1"><a href="{% url "productdetail" pk=dp.id category_name="Deal of the day" %}" class="text-grey-700 fw-600 font-xsss lh-2 ls-0">{{dp.name}}</a></h2>\
                                <h6 class="font-xss ls-3 fw-700 text-current d-flex"><span class="font-xsssss text-grey-500">₹</span>{{dp.list_price|floatformat:2}}<span class="ms-auto text-grey-500 fw-500 font-xsssss">{{dp.unit}}</span></h6>\
                                <div class="progress mt-3 h-5">\
                                    <div class="progress-bar bg-success" role="progressbar" style="width: 25%" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>\
                                </div>\
                                <h4 class="text-grey-600 fw-600 font-xssss mt-2">Sold 4 <span class="font-xssssss">/</span> 20</h4>\
                                <div class="cart-count d-flex mt-4 mb-2">\
                                    <div class="number">\
                                        <span class="minus">-</span>\
                                        <input type="text" class="open-font" value="1">\
                                        <span class="plus">+</span>\
                                    </div>\
                                </div>\
                            </div>\
                        </div>');
                    productsList.append(card);
                }
            }
        });
    });
});

// var owl = $('.owl-carousel');
// owl.owlCarousel();

//function for show +- button and functionality
function item_add(self) {
    var owl = $(self);
    owl.owlCarousel();

    var element_id = self.id.split("-")[0];
    var cate = self.id.split(":")[1];
    owl.trigger('replace.owl.carousel', [$, 0]);
    //owl.replace("." + element_id + "-qty-" + cate);
    //$("." + element_id + "-qty-" + cate).css('display','');
}

function plusBtnClick(element_id, cat_name) {
    console.log("pls btn calling");
    text = parseInt($("#" + element_id + "-qunt_val-" + cat_name).text());
    val = text + 1;
    if (val > 0) {
        $("#" + element_id + "-qunt_val-" + cat_name).empty(val);
        $("#" + element_id + "-qunt_val-" + cat_name).append(val);
    }
}

function minusBtnClick(element_id, cat_name) {
    console.log("minus-btn calling");
    text = parseInt($("#" + element_id + "-qunt_val-" + cat_name).text());
    val = text - 1;
    if (val > 0) {
        $("#" + element_id + "-qunt_val-" + cat_name).empty(val);
        $("#" + element_id + "-qunt_val-" + cat_name).append(val);
    }
}
