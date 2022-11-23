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