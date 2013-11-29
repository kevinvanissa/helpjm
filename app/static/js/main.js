$(document).ready(function(){
    $("#category").change(function(){
        category_srvc = $("#category").val();
        $.post('/servicelist',
            {'category':category_srvc},
            function(data){
                $('#service').empty();
                $('#service').append('<option value="">--- Select a Service --</option>')
                $.each(data,function(i,val){
                $('#service').append('<option value="' + val + 
                        '">' + val + '</option>'); 

                });
                $('#service').focus();
            });
    });


$('#question').maxlength({
alwaysShow: true,
threshold: 10,
warningClass: "label label-warning",
limitReachedClass: "label label-danger",
separator: ' of ',
preText: 'You have ',
postText: ' chars remaining.'
});


$('#review').maxlength({
alwaysShow: true,
threshold: 10,
warningClass: "label label-warning",
limitReachedClass: "label label-danger",
separator: ' of ',
preText: 'You have ',
postText: ' chars remaining.'
});


$('.pleasewait').click(function(){
    $('#myModal').modal()
});

});



function deleteItem(){
    if(confirm("This action will delete the selected item. Are you sure you want to continue?")){
        return true;
}
    return false;
}

function closeItem(){
    if(confirm("This action will close the selected Ask. Are you sure you want to continue ?")){
        return true;
}
    return false;
}

function openItem(){
    if(confirm("This action will open the selected Ask. Are you sure you want to continue ?")){
        return true;
}
    return false;
}



function deleteMultipleItems(){
    if(confirm("This action will delete all the selected friends. Are you sure you want to contine?")){
        return true;
}
    return false;
}

function validateSearchForm(){
        var searchcat = document.forms["search_form"]["category"].value;
        var searchser = document.forms["search_form"]["service"].value;
            if(searchcat == null || searchcat == "" || searchser == null || searchser == "") {
                alert("Please Enter the Category and Service");
                    return false;
            }
    
            return true;  
}



