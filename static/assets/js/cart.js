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

jQuery(document).ready(function () {
    $('.cart-plus-ck').click(function (e) {
        //showLoader();
        e.preventDefault();
        //fieldName = $(this).attr('field');
        const elementId = $(this).attr('id').split('-')[0]
        const size = $(this).attr('id').split(':')[1]
        console.log(elementId);
        domain = window.location.origin
        path_name = '/api/v1/customer/order/add/' //change-this url
        $.ajax({
            type: 'POST',
            url: domain + path_name,
            data: {
                "csrfmiddlewaretoken": g_csrftoken,
                "product": elementId.toString(),
                "quantity": "1",
                "size":size.toString()
            },
            success: function (response) {
                if (response) {
                    console.log(response);
                    //hideLoader();
                    // document.getElementById("dis_price").innerHTML = "₹" + response['amount'];
                    document.getElementById("product-subtotal").innerHTML = "₹" + response['item_dprice']+".00";
                    document.getElementById("grand-total").innerHTML = "Total <span>" + "₹" + response['amount'] + ".00</span>";
                    document.getElementById("grand-subtotal").innerHTML = "Subtotal <span>" + "₹" + response['amount'] + ".00</span>";

                    // document.getElementById(elementId + "-item-sell-price").innerHTML = "₹" + response['item_tprice'];
                    // document.getElementById(elementId + "-item-dis-price").innerHTML = "₹" + response['item_dprice'];
                    // //document.getElementById("quantity").innerHTML = response['qty'];
                    // document.getElementById(elementId + "-name-value").value = response['item_qty'];
                    //$("#"+element_id+"-qunt_val").append(response['cart']['items']['quantity'])
                }
            }
        })
    });
    $('.add-to-cart').click(function (e) {
        e.preventDefault();
        //fieldName = $(this).attr('field');
        const elementId = $(this).attr('id').split('-')[0]
        console.log(elementId);
        domain = window.location.origin
        path_name = '/buy/api/v1/customer/order/add/' //change-this url
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
                    //console.log(response);
                    document.getElementById("cart-amount").innerHTML = "₹" + response['amount'];
                    document.getElementById("quantity").innerHTML = response['qty'];
                    document.getElementById(elementId + "-qunt_val-category").innerHTML = response['item_qty'];
                }
            }
        })
    });

    $('.cart-minus-ck').click(function (e) {
        //showLoader();
        e.preventDefault();
        //fieldName = $(this).attr('field');
        const elementId = $(this).attr('id').split('-')[0]
        const size = $(this).attr('id').split(':')[1]
        console.log(elementId);
        domain = window.location.origin
        path_name = '/api/v1/customer/order/remove/' //change-this url
        $.ajax({
            type: 'POST',
            url: domain + path_name,
            data: {
                "csrfmiddlewaretoken": g_csrftoken,
                "product": elementId.toString(),
                "quantity": "1",
                "size": size.toString()
            },
            success: function (response) {
                if (response) {
                    //hideLoader();
                    //console.log(response);
                    document.getElementById("dis_price").innerHTML = "₹" + response['amount'];
                    document.getElementById("sell_price").innerHTML = "₹" + response['tmax_amount'];
                    document.getElementById("grand-total").innerHTML = "₹" + response['amount'];
                    document.getElementById(elementId + "-item-sell-price").innerHTML = "₹" + response['item_tprice'];
                    document.getElementById(elementId + "-item-dis-price").innerHTML = "₹" + response['item_dprice'];
                    //document.getElementById("quantity").innerHTML = response['qty'];
                    document.getElementById(elementId + "-name-value").value = response['item_qty'];
                    if (response['item_qty'] == 0) {
                        location.reload(true);
                    }
                }
            }
        })
    });
});
