$(document).ready(function() {
    
    date_of_birth = $('#id_personal_detail_form-date_of_birth')[0];
    date_of_birth.type = "date";
    date_of_birth.className = "datepicker";  

  	$('.datepicker').pickadate({
    	selectMonths: true, // Creates a dropdown to control month
    	selectYears: 40,
        max: true,
  	});
    

    $('textarea').addClass('materialize-textarea');
    $('select').material_select();

    //Code for Form Validation
    //console.log($('#id_user_creation_form-username'));

    $('#id_user_creation_form-username').attr("pattern", "[A-z][0-9]{2}[A-z]{2}[0-9]{3}");
    $('#id_education_detail_form-college_passout_year').attr("pattern", "20[0-9]{2}");

    $('#sem_1').attr("required", true);
    $('#sem_2').attr("required", true);
    $('#sem_3').attr("required", true);
    $('#sem_4').attr("required", true);

});

$('#create_account_form').submit(function(event) {
    console.log('hi');

    form_errors = $('#form_errors');
    form_errors.html('');
    var errors = [];
    
    var password1 = $('#id_user_creation_form-password1').val();
    var password2 = $('#id_user_creation_form-password2').val();

    if(password1 != password2) errors.push("Passwords do not match.");
    else if(password1.length < 8) errors.push("The password is too short. It must contain at least 8 characters");

    var gender = $('#id_personal_detail_form-gender').val();
    if(gender=="") errors.push("Gender field is required.");

    var date_of_birth = $('#id_personal_detail_form-date_of_birth').val();
    if(date_of_birth=="") errors.push("Date of Birth field is required.");

    var branch = $('#id_education_detail_form-branch').val();
    if(branch=="") errors.push("Branch field is required.");

    var highest_sem = 4;
    var blank_sems = [];
    var cgpas = {};
    
    for(i=5; i<=10; i++) {
        var sem_id = "#sem_" + i.toString();
        var sem_cgpa =  $(sem_id).val();
        cgpas[i] = sem_cgpa;
        if(sem_cgpa!="") highest_sem = Math.max(highest_sem, i);
    }
    
    for(i=5; i<=highest_sem; i++)
        if(cgpas[i]=="") blank_sems.push(i);

    if(blank_sems.length > 0) {
        var sem_error = "Please enter the CGPA of semester ";
        sem_error += blank_sems.toString();
        errors.push(sem_error);
    }

    for (i=0; i<errors.length; i++)
        console.log(errors[i]);

    var html_str = '';
    if(errors.length > 0){
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

$('#id_education_detail_form-resume').on("change", function(e) {
    var val = $(this).val();
    
    if (!val.match(/(?:pdf)$/)) {
        alert("Please upload your resume in PDF! If you have it another format, you can always print it to PDF!");
    }
    
    else {
        var parent = e.target.closest('.file-field'); 
        elem = parent.getElementsByTagName('span')[1];
        elem.className += " truncate";
        elem.innerHTML = val.split(/(\\|\/)/g).pop()
;
    }
});