$(document).ready(function(){

    /*$('#likes').click(function(){
        var catid;
        catid = $(this).attr("data-catid");
        $.get('/rango/like_category/',{category_id:catid}, function(data){
            $('#like_count').html(data);
            $('#likes').hide();
        });
    });*/
    
    $('#suggestion').keyup(function(){
        var query;
        query = $(this).val();
        $.get('/exercises/suggest_exercises/',{suggestion:query},function(data){
            $('#exercises').html(data);
        });
    });
   
       
   $('#see_all').click(function(){
        $.get('/exercises/see_all/',{},function(data){
            $('#exercises').html(data);
        });
        
    });
            
     
});
