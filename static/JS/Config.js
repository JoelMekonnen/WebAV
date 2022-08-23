  $(document).ready(function () {
    var bar = $('#bar1');
    var percent = $('#percent1');
    $('#submitForm').ajaxForm({
        beforeSubmit: function() {
            document.getElementById("progress_div").style.display="block";
            var percentVal = '0%';
            bar.width(percentVal)
            percent.html(percentVal);
        },
        uploadProgress: function(event, position, total, percentComplete) {
            var percentVal = percentComplete + '%';
            console.log(percentComplete);
            bar.width(percentVal)
            percent.html(percentVal);
        },
        success: function() {
            var percentVal = '100%';
            console.log("success");
            bar.width(percentVal)
            percent.html(percentVal);
        },
        complete: function(xhr) {
            if(xhr.responseText)
            {
                document.getElementById("response").innerHTML = xhr.responseText;
            }
        }
    }); 
  });
  