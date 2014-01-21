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

$(document).ready(function() {
    // $('#previous').click();
    // $('#next').click();

    $('body').on('click', 'span.name-label', select_name);
    $('body').on('click', 'span.clear-label', clear_labels)

    $('body').on('click', 'span.label-1', update_label);
    $('body').on('click', 'span.label-0', update_label);
});
