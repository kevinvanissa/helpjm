$(document).ready(function(){

  $("#feature_div").click(function(){
        window.location = $(this).find("a:first").attr("href");
        return false;
    });

    //alert($('#main-navbar').css("height"));

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


$(document).ready(function(){
  $("address").each(function(){                        
    var embed ="<iframe width='425' height='350' frameborder='0' scrolling='no'  marginheight='0' marginwidth='0'   src='https://maps.google.com/maps?&amp;q="+ encodeURIComponent( $(this).text() ) +"&amp;output=embed'></iframe>";
                                $(this).html(embed);
                            
   });
});


$(document).ready(function(){
	var maxField = 10; //Input fields increment limitation
	var addButton = $('.add_button'); //Add button selector
	var wrapper = $('.field_wrapper'); //Input field wrapper
	var fieldHTML = '<div><input type="text" name="field_name[]" value=""/><a href="javascript:void(0);" class="remove_button" title="Remove field"><img src="/static/img/remove-icon.png"/></a></div>'; //New input field html 
	var x = 1; //Initial field counter is 1
	$(addButton).click(function(){ //Once add button is clicked
		if(x < maxField){ //Check maximum number of input fields
			x++; //Increment field counter
			$(wrapper).append(fieldHTML); // Add field html
		}
	});
	$(wrapper).on('click', '.remove_button', function(e){ //Once remove button is clicked
		e.preventDefault();
		$(this).parent('div').remove(); //Remove field html
		x--; //Decrement field counter
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

$('#description').maxlength({
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


//This is for Tabs
$('#myTab a').click(function (e) {
  e.preventDefault()
  $(this).tab('show')
})

$('#myTab a[href="#profile"]').tab('show')


});

$(window).resize(function () { 
   $('body').css('padding-top', parseInt($('#main-navbar').css("height"))+30);
});

$(window).load(function () { 
   $('body').css('padding-top', parseInt($('#main-navbar').css("height"))+30);         
}); 


function getCalendar(year,month,change){
$.post('/displaycal',
            {'year':year,'month':month,'change':change},
            function(data){
                $('#myCalendar').html(data)                                
                //$.each(data,function(i,val){
                     //});//end first each
            });
}//end getCalendar



function showEvents(year,month,day){
var m_names = new Array("January", "February", "March", 
"April", "May", "June", "July", "August", "September", 
"October", "November", "December");
var daysOfWeek = new Array('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday');

    //alert(day);
    //alert(whichDay(year,month,day));
        $.post('/eventlist',
            {'year':year,'month':month,'day':day},
            function(data){
                $('#myModalLabel').empty();
                $('#eventsfordate').empty();
                
                var wDay = day+" "+m_names[month-1]+", "+year
                var myDate=new Date(wDay);
                var which_day = daysOfWeek[myDate.getDay()]
                //var which_day=whichDay(year,month,day);
                $('#myModalLabel').append(which_day+" "+day+"-"+m_names[month-1]+"-"+year);
                $.each(data,function(i,val){
                    $.each(val, function(j,val2){
                            $('#eventsfordate').append(
                                  "<div class='media'>"+
                    "<a class='pull-left' href='/detail/"+val2.id+"'><img src='/uploads/"+val2.thumbnail+"' width='120px' height='120px'></a>"+
                        "<div class='media-body'>"+
                            "<h4 class='media-heading'><a href='/detail/"+val2.id+"'>"+val2.title+"</a></h4>"+
                            "<b>Venue: </b><span class='detail'>"+val2.venue+
                            "</span><br /><b>Address: </b><span class='detail'>"+val2.address+
                            "</span><br /><b>Parish: </b><span class='detail'>"+val2.parish+
                            "</span><br /><b>Event Start Time: </b><span class='detail'>"+val2.event_start_date+
                        "</span></div>"+
                    "</div>"
                            ); //end append
                    });//end second each
                     });//end first each
            });
    $('#eventModal').modal()
}


function deleteItem(){
    if(confirm("This action will delete the selected item. Are you sure you want to continue?")){
        return true;
}
    return false;
}

function closeItem(){
    if(confirm("This action will close the selected Ask, delete replies and all other information connected to this Ask. \n\n Are you sure you want to continue ?")){
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
        //var title = document.forms["advance_search_form"]["title"].value  
        var elementsForm = document.getElementById("search_form");
        //I had to minus 2 because of the check on button click
        for(var intCounter=0; intCounter < elementsForm.length-2; intCounter++){
            checkValue= elementsForm[intCounter].value;
            //alert(checkValue)
            if (checkValue != ""){
                return true;
            }
        }
        alert("Please enter at least one search field");
        return false;
    }


function validateSearchForm2(){
        //var title = document.forms["advance_search_form"]["title"].value  
        var elementsForm = document.getElementById("search_form");
        //I had to minus 3 because of the check on button click and Anyone
        for(var intCounter=0; intCounter < elementsForm.length-3; intCounter++){
            checkValue= elementsForm[intCounter].value;
            //alert(checkValue)
            if (checkValue != ""){
                return true;
            }
        }
        alert("Please enter at least one search field");
        return false;
    }




function validateEventSearchForm(){
        //var title = document.forms["advance_search_form"]["title"].value  
        var elementsForm = document.getElementById("searchevent");
        for(var intCounter=0; intCounter < elementsForm.length-1; intCounter++){
            checkValue= elementsForm[intCounter].value;
            //alert(checkValue)
            if (checkValue != ""){
                return true;
            }
        }
        alert("Please enter at least one search field");
        return false;
    }






function validateMainSearch(){
    var mainsearch =  document.forms["main_search_form"]["mainsearch"].value
    if (mainsearch == null || mainsearch == ""){
                alert("Enter a Service to Search For! eg., Auto");
                return false;
    }
    return true;
}



