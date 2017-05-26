$(document).ready(function() {
	elem = $('#resume_upload').find('a')[0];
	elem.innerHTML = elem.innerHTML.split(/(\\|\/)/g).pop();
	elem.className = "truncate";
});

$('#id_education_detail_form-resume').on("change", function(event) {
    var val = $(this).val();

    if (!val.match(/(?:pdf)$/)) {
        alert("Please upload your resume in PDF! If you have it another format, you can always print it to PDF!");
        $(this).val('');
    }
});
