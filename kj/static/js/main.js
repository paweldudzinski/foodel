function validateEmail(email) { 
    var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
} 

function isInteger(n) {
    n = parseInt(n);
    return n === +n && n === (n|0);
}

$(document).ready(function() {
    
    $('.cbox').colorbox({rel:'cbox'});
    
    var $container = $('.newest-products')
    
    $container.imagesLoaded( function(){
      $container.masonry({
			itemSelector: '.tile', 
			columnWidth: function(containerWidth) { 
				return 220;
			},
            'gutter': 10,
		});
      var np_div_height = $('.newest-products').height();
      $('.filters section').height(np_div_height);   
    });
    
    $('.search-button').click(function() {
        var value = $('.search-input').val();
        if (value) {
            $('#search-form').submit();
        }
        return false;
    });
    
    $('.ondelete').click(function() {
        var answer = confirm('Na pewno chcesz usunąć?');
        if (!answer) {
            return false;
        }
    });
    
    $('.onedit').click(function() {
        var answer = confirm($(this).attr('rel'));
        if (!answer) {
            return false;
        }
    });
        
    $('.onconfirm').click(function() {
        var answer = confirm($(this).attr('rel'));
        var ID = $(this).attr('id')
        if (!answer) {
            return false;
        }
        $('#product_for_exchange').val(ID);
        $('#exchange-form').submit();
    });
    
    $('#save-user').click(function() {
        var name = $('#name').val();
        var email = $('#remail').val();
        var password = $('#rpassword').val();
        var rpassword = $('#rrpassword').val();
        var terms_and_conditions = $('#terms_and_conditions').is(':checked');

        if (!name || !email) {
            $.jGrowl('Koniecznie trzeba wypełnić nazwę użytkownika i email');
            return false;
        }
        
        if (!validateEmail(email)) {
            $.jGrowl('Email jest nieprawidłowy, czegoś brakuje');
            return false;
        } 
        
        if (!password || !rpassword) {
            $.jGrowl('Oba pola z hasłami muszą być wypełnione');
            return false;
        }
        
        if (password!=rpassword) {
            $.jGrowl('Hasła nam się nie zgadzają...');
            return false;
        }
        
        if (!terms_and_conditions) {
            $.jGrowl('Koniecznie trzeba zaznaczyć ze się akceptuje regulamin');
            return false;
        }
        
        return true;
    });
    
    $('#bargain_type').change(function() {
        var value = $(this).val();
        if (value == 'S') {
            $('#selling-price').show();
            $('#price').val('');
        } else {
            $('#selling-price').hide();
        }
    });
    
    $('#save-product').click(function() {
        var title = $('#title').val();
        var bargain_type = $('#bargain_type').val();
        var availability_type = $('#availability_type').val();
        var shipping_type = $('#shipping_type').val();
        var description = $('#description').val();
        var category = $('#category').val();
        var subcategory = $('#category').val();
        var quantity = $('#quantity').val();
        var price = $('#price').val();
        
        if (!title) {
            $.jGrowl('Koniecznie trzeba wypełnić nazwę produktu.');
            return false;
        }
        
        if (!category || !subcategory) {
            $.jGrowl('Koniecznie trzeba wybrać kategorię i podkategorię.');
            return false;
        }
        
        if (!bargain_type) {
            $.jGrowl('Koniecznie trzeba wybrać co chcesz z tym zrobić.');
            return false;
        }
        
        if ((bargain_type == 'S') && (!price)) {
            $.jGrowl('Koniecznie trzeba podać cenę.');
            return false;
        }
        
        if (!availability_type) {
            $.jGrowl('Proszę, wybierz co z dostępnością produktu');
            return false;
        }
        
        if (!shipping_type) {
            $.jGrowl('Proszę, wybierz co z ewentualną dostawą produktu');
            return false;
        }
        
        if (!description) {
            $.jGrowl('Koniecznie dodaj krótki opis');
            return false;
        }
        
        if (!isInteger(quantity)) {
            $.jGrowl('Ilość sztuk musi być liczbą');
            return false;
        }
        
        return true;
    });
    
    $('.grade').live('click', function() {
        orderID = $(this).attr('rel');
        $.get('/ocen-order/'+orderID, function(data) {
            $('#grade-modal').html(data);
        });
    });
    
    $('.grade-row').live('click', function() {
        var grade = $(this).attr('rel').split('.')[0];
        var order = $(this).attr('rel').split('.')[1];
        var url = '/zapisz-ocene/'+order+'/'+grade;
        window.location = url;
    });
    
    $('#quantity').change(function() {
        var quantity = parseFloat($(this).val());
        var price = $('#unit-price-tag').html();
        if (!price) {
            return false;
        }
        price = parseFloat(price);
        $('#price-tag').html(quantity*price);
    });
    
    $('.select-filter').change(function() {
        $('#transactions-filter').submit();
    });
    
    $('#wojewodztwo').live('change', function() {
        var value = $(this).val();
        $('#cities-container').html('<br /><br />');
        $('#city').find('option').remove().end().append('<option value="">--- wybierz kategorię powyżej ---</option>').val('');
        if (value) {
            $.get('/doladuj-miasta/'+value, function(data) {
                $('#cities-container').html(data);
            });
        }
    });
    
    $('#category').live('change', function() {
        var value = $(this).val();
        $('#subcategory-container').html('<br /><br />');
        $('#subcategory2').find('option').remove().end().append('<option value="">--- wybierz kategorię powyżej ---</option>').val('');
        if (value) {
            $.get('/doladuj-podkategorie/'+value, function(data) {
                $('#subcategory-container').html(data);
            });
        }
    });
    
    $('#subcategory').live('change', function() {
        var value = $(this).val();
        $('#subcategory2-container').html('<br /><br />');
        if (value) {
            $.get('/doladuj-podkategorie2/'+value, function(data) {
                $('#subcategory2-container').html(data);
            });
        }
    });
    
    $('#base_coupled_cat').change(function() {
        $('.coupled-categories').html('');
        var value = $(this).val();
        if (value) {
            $.get('/doladuj-sparowane/'+value, function(data) {
                $('.coupled-categories').html(data);
            });
        }
    });
    
    $('.product-photo').hover(
        function() {
            $(this).find('.product-apla-opacity').show();
            $(this).find('.product-apla').show();
        },
        function() {
            $(this).find('.product-apla-opacity').hide();
            $(this).find('.product-apla').hide();
        }
    );
    
    $('#save-event').click(function() {        
        var title = $('#title').val();
        var description = $('#description').val();
        var date_from = $('#date_from').val();
        var city = $('#city').val();
        
        if (!title) {
            $.jGrowl('Koniecznie trzeba wypełnić tytuł wydarzenia.');
            return false;
        }
        
        if (!description) {
            $.jGrowl('Koniecznie trzeba wypełnić jakiś krótki opis.');
            return false;
        }
        
        if (!date_from) {
            $.jGrowl('Koniecznie trzeba wypełnić datę rozpoczęcia wydarzenia.');
            return false;
        }
        
        if (!city) {
            $.jGrowl('Koniecznie trzeba wypełnić miejsce wydarzenia.');
            return false;
        }
        
    });
    
    $('#date_from').datepicker({
        format: "dd-mm-yyyy",
        todayBtn: true,
        language: "pl",
        todayHighlight: true,
        autoclose: true
    });
    
    $('#date_to').datepicker({
        format: "dd-mm-yyyy",
        todayBtn: true,
        language: "pl",
        todayHighlight: true,
        autoclose: true
    });
     
});
