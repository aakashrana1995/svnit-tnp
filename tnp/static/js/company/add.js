$(document).ready(function() {
	$('textarea').addClass('materialize-textarea');
	$('#down_left').css('margin-top', '75px');
	
    $('select[required]').removeAttr('required');

  	crpdate = $('#id_company_form-crpdate')[0];
    crpdate.type = "date";
    crpdate.className = "datepicker";
  
    deadline_date = $('#id_consent_deadline_form-deadline_date')[0];
    deadline_date.type = "date";
    deadline_date.className = "datepicker";  

    deadline_time = $('#id_consent_deadline_form-deadline_time')[0];
    deadline_time.type = "time";
    deadline_time.className = "timepicker";  

  	$('.datepicker').pickadate({
    	selectMonths: true, // Creates a dropdown to control month
    	selectYears: 5, // Creates a dropdown of 5 years to control year
        //format: 'yyyy-mm-dd',
  	});

    $('.timepicker').pickatime({
        autoclose: false,
        twelvehour: true,
        default: 'now',
    });
    

	elems = document.getElementsByTagName('textarea');
	for (i=0; i<elems.length; i++)
		elems[i].style.height = "70px";
	
    $('select').material_select();

    $('#cgpa_upto_semester')[0].innerHTML = 'CGPA Upto Semester <input type="hidden" value="cgpa_upto_semester" name="A"> <div class="input-field inline"> <input type="number" min="-10" max="-1" value="-3" name="A" style="width: 30px; text-align: center;"> </div>';
    $('#cgpa_of_semester')[0].innerHTML = 'CGPA Of Semester <input type="hidden" value="cgpa_of_semester" name="C"> <div class="input-field inline"> <input type="number" min="-10" max="-1" value="-3" name="C" style="width: 30px; text-align: center;"> </div>';
});


$('#add_company_form').submit(function(event) {
    form_errors = $('#form_errors');
    form_errors.html('');
    var errors = [];

    job_type = $('#id_job_form-job_type').val();
    if(job_type=="") errors.push("Please select a job type. Select 'Other' if no category matches.");

    eligible_branches = $('#id_job_form-eligible_branches').val();
    if(eligible_branches=="") errors.push("Please select eligible branches.");

    consent_deadline = $('#id_consent_deadline_form-deadline_date').val();
    if(consent_deadline=="") errors.push('Please select a consent deadline date.');

    for (i=0; i<errors.length; i++)
        console.log(errors[i]);

    var html_str = '';
    if(errors.length > 0) {
        $('body').scrollTop(0);
        html_str += '<ul class="collection red-text">';
        for(i=0; i<errors.length; i++)
            html_str += '<li class="collection-item">' + errors[i] + '</li>';

        html_str += '</ul>';
        form_errors.append(html_str);

        alert("Please remove these form errors");
        event.preventDefault();
    }
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


$('#id_attachment_form-file').on("change", function(e) {
    files_data = e.target.files;
    if(files_data.length>1)
        string = files_data.length + " files";
    else
        string = files_data[0].name;

    var parent = e.target.closest('.file-field');
    parent.getElementsByTagName('span')[1].innerHTML = string;
});



Sortable.create(A, {
  group: "sorting",
  sort: true,
  onAdd: function (evt) {
        var itemEl = evt.item;
        elems = itemEl.getElementsByTagName('input');
        for (var i=0; i<elems.length; i++) {
            elems[i].name = "A";
        }
    },
});

Sortable.create(B, {
  group: "sorting",
  sort: true,
  onAdd: function (evt) {
        var itemEl = evt.item;
        elems = itemEl.getElementsByTagName('input');
        for (var i=0; i<elems.length; i++) {
            elems[i].name = "B";
        }
    },
});

Sortable.create(C, {
  group: "sorting",
  sort: true,
  onAdd: function (evt) {
        var itemEl = evt.item;
        elems = itemEl.getElementsByTagName('input');
        for (var i=0; i<elems.length; i++) {
            elems[i].name = "A";
        }
    },
});

