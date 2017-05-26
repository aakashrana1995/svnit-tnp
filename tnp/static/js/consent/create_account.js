$('#id_education_detail_form-resume').on("change", function(e) {
    var val = $(this).val();
    
    if (!val.match(/(?:pdf)$/)) {
        alert("Please upload your resume in PDF! If you have it another format, you can always print it to PDF!");
    }
    
    else {
        var parent = e.target.closest('.file-field'); 
        elem = parent.getElementsByTagName('span')[1];
        elem.className += " truncate";
        elem.innerHTML = val.split(/(\\|\/)/g).pop();
    }
});