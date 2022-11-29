var imagesObject = [];

function configure() {
    Webcam.set({
        width: 500,
        height: 450,
        dest_width: 500,
        dest_height: 450,
        image_format: 'jpeg',
        jpeg_quality: 90
    })
    Webcam.attach("#my_camera");
}

function take_snapshot() {
    // take snapshot and get image data
    document.getElementById('my_camera').classList.toggle("effect");

    document.getElementById("embeddingsBtn").style.display = "none";

    Webcam.snap(function(data_uri) {
        // display results in page

        displayImgData(data_uri);
        addImage(data_uri)
    });
}

function addImage(imgData) {
    imagesObject.push(imgData);
    displayNumberOfImgs();
    localStorage.setItem("images", JSON.stringify(imagesObject));
}

function displayImgData(imgData) {
    var span = document.createElement('li');
    span.innerHTML = '<img class="thumb" src="' + imgData + '"/>';
    document.getElementById('list').insertBefore(span, null);
}

function displayNumberOfImgs() {
    if (imagesObject.length > 0) {

        document.getElementById("state").innerHTML = imagesObject.length + " image" + ((imagesObject.length > 1) ? "s" : "") + " stored in your browser";



        if (checkImages(imagesObject)) {
            document.getElementById('snapDiv').style.display = 'none';
            document.getElementById("embeddingsBtn").style.display = "block";
            Swal.fire({
                title: '<strong>Only 8 snaps allowed</strong>',
                icon: 'info',
                showCloseButton: true,
                showCancelButton: true,
                focusConfirm: false,
                confirmButtonText: '<i class="fa fa-thumbs-up"></i> Great!',
                confirmButtonAriaLabel: 'Thumbs up, great!',
            })
        } else {
            document.getElementById('snapDiv').style.display = 'block';
        }

        console.log("ARR LENGTH ", checkImages(imagesObject))

    } else {
        document.getElementById("state").innerHTML = "No images stored in your browser.";
    }
}

//To check if an array is empty using javascript
function checkImages(array) {
    //If it's not an array, return FALSE.
    if (!Array.isArray(array)) {
        return FALSE;
    }
    //If it is an array, check its length property
    if (array.length == 8) {
        //Return TRUE if the array is empty
        return true;
    }
    //Otherwise, return FALSE.
    return false;
}

function deleteImages() {
    imagesObject = [];
    console.log("remove")
    localStorage.removeItem("images");
    displayNumberOfImgs()
    document.getElementById('list').innerHTML = "";
    document.getElementById("embeddingsBtn").style.display = "none";
}

function loadFromLocalStorage() {
    var images = JSON.parse(localStorage.getItem("images"))

    console.log(images)

    if (images && images.length > 0) {
        imagesObject = images;

        displayNumberOfImgs();
        images.forEach(displayImgData);
    }
}

function post(value) {

    console.log(value)
    Swal.fire({
        imageUrl: 'https://i.gifer.com/DzUh.gif',
        imageWidth: 400,
        imageHeight: 200,
        showConfirmButton: false
    })

    var images = JSON.parse(localStorage.getItem("images"))
    var params = {}
    for (var i = 0; i < images.length; i++) {
        var strImage = images[i].replace(/^data:image\/[a-z]+;base64,/, "");
        params["image" + (i + 1)] = strImage;
    }
    if(value=='login'){
        url = '/application/'
    }
    else{
        url = '/application/register_embedding'
    }
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = url;

    for (const key in params) {
        if (params.hasOwnProperty(key)) {
            const hiddenField = document.createElement('input');
            hiddenField.type = 'hidden';
            hiddenField.name = key;
            hiddenField.value = params[key];

            form.appendChild(hiddenField);
        }
    }

    document.body.appendChild(form);
    form.submit();
}
const errorElement = document.querySelector('#error_msg');
const codeElement = document.querySelector('#status_code');
//console.log(codeElement.value)
if(codeElement){
    console.log(codeElement.value)
}
if(codeElement && codeElement.value == 200){
  Swal.fire({
    position: 'top-end',
    icon: 'success',
    title: errorElement.value,
    showConfirmButton: false,
    timer: 1500
  })
}
if(codeElement && codeElement.value == 401){
    Swal.fire({
        icon: 'error',
        title: 'Oops...',
        text: errorElement.value,
        footer: '<a href="">Why do I have this issue?</a>'
      })
  }
  

document.getElementById('deleteImgs').addEventListener("click", deleteImages);
//loadFromLocalStorage();
document.getElementById("embeddingsBtn").style.display = "none";