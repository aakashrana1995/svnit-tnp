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
    $('#id_user_creation_form-username').attr("pattern", "[A-z][0-9]{2}[A-z]{2}[0-9]{3}");
    $('#id_education_detail_form-college_passout_year').attr("pattern", "20[0-9]{2}");
    $('#id_education_detail_form-ssc_passing_year').attr("pattern", "20[0-9]{2}");
    $('#id_education_detail_form-hsc_passing_year').attr("pattern", "20[0-9]{2}");

    $('#id_personal_detail_form-current_pincode').attr("pattern", "[0-9]{6}");
    $('#id_personal_detail_form-permanent_pincode').attr("pattern", "[0-9]{6}");

    var board_dict = {
            "Central Board of Secondary Education (CBSE)": null,
            "Indian Certificate for Secondary Education (ICSE)": null,
            "Board of Higher Secondary Education, Delhi":null,
            "Andhra Pradesh Board of Secondary Education": null,
            "Board of Intermediate Education, Andhra Pradesh (BIEAP)": null,
            "Board of Secondary Education, Assam": null,
            "Assam Higher Secondary Education Council": null,
            "Bihar School Examination Board (BSEB)": null,
            "Board of Secondary Education Kant Shahjahanpur Uttar Pradesh": null,
            "Board of High School and Intermediate Education Uttar Pradesh (UPMSP)": null,
            "Madhya Pradesh Board of Secondary Education (MPBSE)": null,
            "Board of Secondary Education, Rajasthan": null,
            "Chhattisgarh Board of Secondary Education (CGBSE)": null,
            "Central Board of Education Ajmer New Delhi": null,
            "Central Board of Secondary Education": null,
            "Goa Board of Secondary & Higher Secondary Education": null,
            "Gujarat Secondary and Higher Secondary Education Board (GSHSEB | GSEB)": null,
            "Haryana Board of School Education": null,
            "Himachal Pradesh Board of School Education": null,
            "Jharkhand Academic Council": null,
            "Jammu and Kashmir State Board of School Education": null,
            "Karnataka Secondary Education Examination Board (KSEEB)": null,
            "Kerala Higher Secondary Examination Board (KHSEB)": null,
            "Maharashtra State Board of Secondary and Higher Secondary Education": null,
            "Meghalaya Board of School Education": null,
            "Mizoram Board of School Education": null,
            "Nagaland Board of School Education": null,
            "National Institute of Open Schooling": null,
            "Orissa Board of Secondary Education": null,
            "Orissa Council of Higher Secondary Education": null,
            "Punjab School Education Board (PSEB)": null,
            "Tamil Nadu Board of Secondary Education (TNBSE)": null,
            "Tripura Board of Secondary Education": null,
            "Telangana Board of Intermediate Education": null,
            "Telangana Board of Secondary Education": null,
            "Uttarakhand Board of School Education": null,
            "West Bengal Board of Secondary Education (WBBSE)": null,
            "West Bengal Council of Higher Secondary Education (WBCHSE)": null,
        }

    $('#id_education_detail_form-ssc_board_name').addClass('autocomplete');
    $('#id_education_detail_form-ssc_board_name').attr('autocomplete', 'off');

    $('#id_education_detail_form-hsc_board_name').addClass('autocomplete');
    $('#id_education_detail_form-hsc_board_name').attr('autocomplete', 'off');

    $('input.autocomplete').autocomplete({    
        data: board_dict,
        limit: 5, // The max amount of results that can be shown at once. Default: Infinity.
        minLength: 1, // The minimum length of the input for the autocomplete to start. Default: 1.
    });

    $('#id_education_detail_form-ssc').attr("min", "0");
    $('#id_education_detail_form-ssc').attr("max", "100");

    $('#id_education_detail_form-hsc').attr("min", "0");
    $('#id_education_detail_form-hsc').attr("max", "100");

    $('#sem_1').attr("required", true);
    $('#sem_2').attr("required", true);
    //$('#sem_3').attr("required", true);
    //$('#sem_4').attr("required", true);

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