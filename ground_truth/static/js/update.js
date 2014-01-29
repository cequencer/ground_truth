function update_label(){
    var reference = this;   //important

    console.log($(reference).attr('class'));
    console.log($(reference).attr('id'));

    $.post('/align/update_label', 
    {
        'label_class': $(reference).attr('class'), 
        'selected_id': $(reference).attr('id')
    }, 
    function(res){
      if(res == true){
        console.log('Success!');
        $(reference).toggleClass('label-1 label-0');
      }
      else{
        console.log("There's some unexpected error, please try again later!");
      }
    });
}

function select_name(){
    var token_id = $(this).attr('id').split('-')[1];
    var fn_id = '#FN-' + token_id;
    var ln_id = '#LN-' + token_id;

    var fn_reference = $(fn_id);
    var ln_reference = $(ln_id);

    $.post('/align/select_name', 
    {
        'selected_id': token_id
    }, 
    function(res){
      if(res == true){
        console.log('Success!');
        fn_reference.attr('class', 'label-button label-1');    
        ln_reference.attr('class', 'label-button label-1');    
        
      }
      else{
        console.log("There's some unexpected error, please try again later!");
      }
    });
}

function clear_labels(){
    var token_id = $(this).attr('id').split('-')[1];
    
    var fn_id = '#FN-' + token_id;
    var ln_id = '#LN-' + token_id;
    var dl_id = '#DL-' + token_id;
    var ti_id = '#TI-' + token_id;
    var vn_id = '#VN-' + token_id;
    var yr_id = '#YR-' + token_id;

    $.post('/align/clear_labels', 
    {
        'selected_id': token_id
    }, 
    function(res){
      if(res == true){
        console.log('Success!');
        $(fn_id).attr('class', 'label-button label-0');
        $(ln_id).attr('class', 'label-button label-0');
        $(dl_id).attr('class', 'label-button label-0');
        $(ti_id).attr('class', 'label-button label-0');
        $(vn_id).attr('class', 'label-button label-0');
        $(yr_id).attr('class', 'label-button label-0');
        
      }
      else{
        console.log("There's some unexpected error, please try again later!");
      }
    });
}

function change_mode(){
    // var reference = this;   //important

    $.post('/validate/change_mode', 
    {
        'mode': $(this).attr('class'),
    }, 
    function(res){
      if(res == true){
        console.log('Mode toggle Success!');
        location.reload();
        // $(this).toggleClass('mode-on mode-off');
      }
      else{
        console.log("There's some unexpected error, please try again later!");
      }
    });
}

$(document).ready(function() {
    $('body').on('click', 'div.pagination_single_record', function() {
       var selected_id = $(this).attr('id');
        var page_id = selected_id.split('-')[1];
        window.location = '/align/align/' + page_id;
    });

    $('body').on('click', 'div.pagination_prev_page', function() {
        var cur_page_id = parseInt(window.location.toString().split('/').pop());
        if(!cur_page_id){   //default page = 0
            window.location = '/align/page/';
        }
        else if(cur_page_id-1 == 0){
            window.location = '/align/page/';    
        }
        else{
            window.location = '/align/page/' + (cur_page_id-1);    
        }
        
    });
    $('body').on('click', 'div.pagination_next_page', function() {
        var cur_page_id = parseInt(window.location.toString().split('/').pop());
        if(!cur_page_id){   //default page = 0
            window.location = '/align/page/1';
        }
        else{
            window.location = '/align/page/' + (cur_page_id+1);
        }
    });

    $('body').on('click', 'span.name-label', select_name);
    $('body').on('click', 'span.clear-label', clear_labels)

    $('body').on('click', 'span.label-1', update_label);
    $('body').on('click', 'span.label-0', update_label);

    $('body').on('click', 'span.mode', change_mode);    

    $('li.token-li')
      .mouseover(function() {
        $(this).addClass('cur-li');
      })
      .mouseout(function() {
        $(this).removeClass('cur-li');
      });
});
