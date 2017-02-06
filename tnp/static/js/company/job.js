// Used for truncating extra text and putting and ellipsis(...) in the end.
$(function(){
        $('.truncate-main').succinct({
            size: 240,
        });
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


