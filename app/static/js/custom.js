function validateFileType(input){
	var fileName = document.getElementById("fileName").value;
  var idxDot = fileName.lastIndexOf(".") + 1;
  var extFile = fileName.substr(idxDot, fileName.length).toLowerCase();
  if (extFile=="jpg" || extFile=="jpeg" || extFile=="png"){
		$('#fileName').attr('class', 'form-control is-valid');
		var reader = new FileReader();
    reader.onload = function (e) {
        $('#showImg')
            .attr('src', e.target.result)
						.height(200);
    };

    reader.readAsDataURL(input.files[0]);
		return true;
  } else{
		$("#fileName").attr('class', 'form-control is-invalid');
		$('#showImg').attr('src', '#');
		return false;
  }
}
