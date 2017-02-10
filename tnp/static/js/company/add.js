$(document).ready(function() {
	$('textarea').addClass('materialize-textarea');
	
	$('#down_left').css('margin-top', '75px');
	
	crpdate = $('#id_company_form-crpdate')[0];
	crpdate.type = "date";
	crpdate.className = "datepicker";

	deadline = $('#id_consent_deadline_form-deadline')[0];
	deadline.type = "date";
	deadline.className = "datepicker";

  	$('.datepicker').pickadate({
    	selectMonths: true, // Creates a dropdown to control month
    	selectYears: 5 // Creates a dropdown of 5 years to control year
  	});
    

	elems = document.getElementsByTagName('textarea');
	for (i=0; i<elems.length; i++) {
		elems[i].style.height = "70px";
	}
	
  $('select').material_select();

  $('#cgpa_upto_semester')[0].innerHTML = 'CGPA Upto Semester <div class="input-field inline"> <input type="number" value="6" style="width: 30px; text-align: center;"> </div>';
  $('#cgpa_of_semester')[0].innerHTML = 'CGPA Of Semester <div class="input-field inline"> <input type="number" value="6" style="width: 30px; text-align: center;"> </div>';

});


 $('#add_more').click(function() {
    var form_idx = $('#id_job_location-TOTAL_FORMS').val();
    $('#job_location_formset').append($('#empty_form').html().replace(/__prefix__/g, form_idx));
    $('#id_job_location-TOTAL_FORMS').val(parseInt(form_idx) + 1);
});

 $('#job_location_formset').on("click", ".remove", function(e) {
	var elem = e.target.closest('.element');
	elem.remove();

	var form_idx = $('#id_job_location-TOTAL_FORMS').val();
	$('#id_job_location-TOTAL_FORMS').val(parseInt(form_idx) - 1);
});


$('#attachment_formset').on("click", ".delete_file", function(e) {
	var elem = e.target.closest('.element');
	elem.remove();
    
    var form_idx = $('#id_attachment-TOTAL_FORMS').val();
    $('#id_attachment-TOTAL_FORMS').val(parseInt(form_idx) - 1);
});


$('#add_more_files').click(function() {
    var form_idx = $('#id_attachment-TOTAL_FORMS').val();
    $('#attachment_formset').append($('#empty_form_attachment').html().replace(/__prefix__/g, form_idx));
    $('#id_attachment-TOTAL_FORMS').val(parseInt(form_idx) + 1);
});


$('#attachment_formset').on("change", ".filename", function(e) {
	filepath = e.target.value;
    arr = filepath.split('\\');
    filename = arr[arr.length-1];
    
    var parent = e.target.closest('.file-field');
    console.log(parent);
    parent.getElementsByTagName('span')[1].innerHTML = filename;
});

$('#timepicker').pickatime({
    autoclose: true,
    twelvehour: true,
    default: 'now'
  });


Sortable.create(A, {
  group: "sorting",
  sort: true
});

// sort: false
Sortable.create(B, {
  group: "sorting",
  sort: true
});

Sortable.create(C, {
  group: "sorting",
  sort: true
});