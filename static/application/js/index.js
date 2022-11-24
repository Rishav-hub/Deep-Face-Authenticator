const textInputs = document.querySelectorAll("input");
const passwordInput = document.querySelector('.password-input');
const eyeBtn = document.querySelector('.eye-btn');
const signUpBtn = document.querySelector('.sign-up-btn');
const signInBtn = document.querySelector('.sign-in-btn');
const signUpForm = document.querySelector('.sign-up-form');
const signInForm = document.querySelector('.sign-in-form');



textInputs.forEach(textInput =>{
    textInput.addEventListener("focus",()=>{
        let parent = textInput.parentNode;
        parent.classList.add("active");
    });
    textInput.addEventListener("blur",()=>{
        let parent = textInput.parentNode;
        parent.classList.remove("active");
    });
});

eyeBtn.addEventListener("click",()=>{
    if(passwordInput.type === 'password'){
        passwordInput.type = 'text';
        eyeBtn.innerHTML = "<i class='uil uil-eye'></i>"
    }
    else{
        passwordInput.type = 'password';
        eyeBtn.innerHTML = "<i class='uil uil-eye-slash'></i>"
    }
});

signUpBtn.addEventListener("click",()=>{
    signInForm.classList.add('hide');
    signUpForm.classList.add('show');
    signInForm.classList.remove('show');
    
});

signInBtn.addEventListener("click",()=>{
    signInForm.classList.remove('hide');
    signUpForm.classList.remove('show');
    signInForm.classList.add('show');
});

const errorElement = document.querySelector('#error_msg');
const codeElement = document.querySelector('#status_code');
if(codeElement.value == 404){
    swal("Oops!", errorElement.value, "error"); 
}

/* var myInput = document.getElementById("error_msg");
    setTimeout(() => {
        if (myInput && myInput.value) {
            console.log(myInput.value)
            alert(myInput.value);
          }
      }, 3000)
      console.log(myInput.value)
      $('#register_form').submit(function(){
    $.ajax({
      url: '/auth/register',
      type: 'POST',
      data : $('#register_form').serialize(),
      success: function(){
        console.log('form submitted.');
      }
    });
    return false;
});


var frm = $('#register_form');


    frm.submit(function (e) {

        e.preventDefault();

        $.ajax({
            type: frm.attr('method'),
            url: frm.attr('action'),
            data: frm.serialize(),
            success: function (data) {
                console.log('Submission was successful.');
                console.log(data);
            },
            error: function (data) {
                console.log('An error occurred.');
                var myInput = document.getElementById("error_msg");
                if (myInput && myInput.value) {
                    console.log(myInput.value)
                    alert(myInput.value);
                  }
            },
        });
    });
    */ 