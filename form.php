<!DOCTYPE html>
<html>
<head>
<script>

var canvas = document.getElementById('canvas');
var context = canvas.getContext('2d');
var video = document.getElementById('video');



// Get access to the camera!
if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    // Not adding `{ audio: true }` since we only want video now
    navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
        //video.src = window.URL.createObjectURL(stream);
        video.srcObject = stream;
        video.play();
    });
}


// Trigger photo take
document.getElementById("snap").addEventListener("click", function() {
	context.drawImage(video, 0, 0, 640, 480);
});
function validateForm() {
  var name = document.forms["myForm"]["fname"].value;
  var num = document.forms["myForm"]["erno"].value;
  if (name == "" && num == "") {
    alert("values must be filled out");
    return false;
  }
  else if (name == "") {
    alert("Name must be filled out");
    return false;
  }
  else if(num == ""){
	  alert("Enrollment Number must be filled");
	  return false;
  }
  else{
	/*const constraints = {	video: true	};

	const video = document.querySelector('video');

	navigator.mediaDevices.getUserMedia(constraints).
	then((stream) => {video.srcObject = stream});*/
	
	
	alert("opening camera");
    return true;
  }
}

function isNumberKey(evt){
    var charCode = (evt.which) ? evt.which : evt.keyCode
    if (charCode > 31 && (charCode < 48 || charCode > 57))
        return false;
    return true;
}

function test(){
	$.ajax({
  type: "POST",
  url: "~/InstanceIT_face_recognition.py",
  data: { param: text}
}).done(function( o ) {
   // do something
   alert("done");
});
	
}
</script>
</head>
<body>

<form name="myForm"  onsubmit="return validateForm()" method="post">
  Enrollment Number : <input type="integer" name="erno" onkeypress="return isNumberKey(event)"><br/><br/>
  Name              : <input type="text" name="fname" ><br/><br/>
  <input type="submit" value="Register" >
</form>

<video id="video" width="640" height="480" autoplay></video>
<button id="snap">Snap Photo</button>
<canvas id="canvas" width="640" height="480"></canvas>

<button onclick="test()">test</button>

</body>
</html>
