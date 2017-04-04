
// Runs on page load to determine the type of button (Apply or Cancel or Disabled)
$(document).ready(function() {
    var button = document.getElementById('consent');
    setButtonProperties(button, button.name);
});

//Takes the button and formats it according to its state
function setButtonProperties(button, targetName) {
    if(targetName == 'apply') {
        button.className = "waves-effect waves-light grey darken-2 grey-text text-lighten-5 btn-large";
        button.name = "apply";
        document.getElementById("consent").childNodes[2].nodeValue = "Apply Consent";
        document.getElementById("button_icon").innerHTML = "send";
    }
    else if(targetName == 'cancel'){
        button.className = "waves-effect waves-light red darken-2 red-text text-lighten-5 btn-large";
        button.name = "cancel";
        document.getElementById("consent").childNodes[2].nodeValue = "Cancel Consent";
        document.getElementById("button_icon").innerHTML = "clear";
    }
    else if(targetName == 'disabled_applied') {
        button.className = "btn-large green darken-2 disabled";
        button.name = "disabled_applied";
        document.getElementById("consent").childNodes[2].nodeValue = "Consent Applied";
        document.getElementById("button_icon").innerHTML = "timer_off"; 
    }
    else {
        button.className = "btn-large red darken-2 disabled";
        button.name = "disabled_not_applied";
        document.getElementById("consent").childNodes[2].nodeValue = "Consent Not Applied";
        document.getElementById("button_icon").innerHTML = "timer_off"; 
    }
}

// Used for truncating extra text and putting an ellipsis(...) in the end.
$(function(){
        $('.truncate-main').succinct({
            size: 240,
        });
    });

// This function creates the hover effect by clicking on the elements that activates the card-reveal div.
$(function(e) {
    $('.card').hover(
        function() {
            $(this).children().first().click();
        }, function() {
            $(this).find('.my-card-reveal .card-title').click();
        }
    );
});

/* This function listens to the the clicks on the card title and reveals/hides the 
 card-reveal element accordingly. */
$(document).ready(function() {

    $(document).on('click.card', '.card', function (e) {

   	   	if ($(this).find('> .my-card-reveal').length) {
        if ($(e.target).is($('.my-card-reveal .card-title')) ||
         		$(e.target).is($('.my-card-reveal .card-title i'))) {
          	// Make Reveal animate down and display none
          	$(this).find('.my-card-reveal').velocity( 
          		{translateY: 0}, {
             		duration: 300,
             		queue: false,
             		easing: 'easeInOutQuad',
              		complete: function() { $(this).css({ display: 'none'}); }
            	}
          	);
          	$(e.target).closest('.card').css('height', '140px');
        }
        else if ($(e.target).is($('.card .activator')) ||
                 $(e.target).is($('.card .activator i')) ) {
          	$(e.target).closest('.card').css('height', '300px').velocity({duration: 50});
          	$(e.target).closest('.card').css('overflow', 'hidden');
          	$(this).find('.my-card-reveal').css({'display': 'block'}).velocity("stop", false).velocity(
          		{translateY: '-100%'}, {
          				duration: 300, 
          				queue: false, 
          				easing: 'easeInOutQuad'
          			}
          		);
        	}
      	}
    });
 });


$("#consent").click(function(e) {
    e.preventDefault();
    var curr_url = window.location.pathname;
    var url_arr = curr_url.split('/');
    var job = url_arr[url_arr.length-2];

    var divName = e.target.name;
    var url, toastMsg, targetName;
    if(divName=='apply') {
      url = '/consent/apply?job=' + job;
      toastMsg = 'Consent successfully applied!';
      targetName = 'cancel';
    }
    else {
      url = '/consent/cancel?job=' + job;
      toastMsg = 'Consent successfully cancelled!';
      targetName = 'apply';
    }

    $.ajax({
        type: "GET",
        url: url,
        contentType: 'application/json; charset=utf-8',
        success: function(result) {
            Materialize.toast(toastMsg, 2000, 'rounded');
            setButtonProperties(e.target, targetName);
        },
        error: function(result) {
            Materialize.toast('Some error has occured. Please try again!', 2000, 'rounded');
        }
    });
});
