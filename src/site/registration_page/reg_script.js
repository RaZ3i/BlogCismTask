const RegForm = document.querySelector(".reg_form");

const regBtn = document.querySelector(".reg_btn");
const backBtn = document.querySelector(".back_btn");

const loginField = document.querySelector('[name="username"]');
const emailField = document.querySelector('[name="email"]');
const passwordField = document.querySelector('[name="password"]');

const loginStatus = document.querySelector('[name="first_input"]')
const emailStatus = document.querySelector('[name="second_input"]')
const passwordStatus = document.querySelector('[name="third_input"]')

const reg_login = /^(?!.*\W)(?=.*?[0-9])(?!.*\W)(?=.*?[A-Z])(?!.*\W)(?=.*?[a-z]).{3,16}$/;
const reg_email = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
const reg_pass = /^(?=.*?[0-9])(?=.*?[A-Z])(?=.*?[a-z])(?=.*?\W).{8,30}$/;


RegForm.addEventListener("input", ValidateForm)
RegForm.addEventListener("submit", e=>{
    e.preventDefault();
})
regBtn.addEventListener("click", SubmitRegistration)
backBtn.addEventListener("click", function() {
    window.location.replace("http://127.0.0.1:5500/src/site/authenticate_page/authentication_page.html");
})

function ValidateForm() {
    deletSpace();
    // Hints();
    LightFields();
    if (reg_login.test(loginField.value) == true && 
        reg_pass.test(passwordField.value) == true && 
        reg_email.test(emailField.value) == true) {
        regBtn.removeAttribute("disabled");
    }
    else {
        regBtn.setAttribute("disabled", "true");
    }
}

async function SubmitRegistration() {
    const new_data = {
        username: loginField.value,
        email: emailField.value,
        hash_password: passwordField.value
    }
    new_user = JSON.stringify(new_data, null, '\t')
    ClearField();
    // ждем ответ с сервера
    try {
        let response = await fetch("http://localhost:8087/auth/register/", {
            mode: 'cors',
            method: "POST",
            body: new_user,
            headers: { //необходимые заголовки из документации API 
                // 'Accept': 'application/json',
                'Content-type': 'application/json',
            },
        });
        // если с ответом все ОК, то получаем из него JSON
        if(response.ok) {
            const json = await response.json();
            if (json.success) {
                window.location.replace("http://127.0.0.1:5500/src/templates/home_page.html")
            }
            else if (!json.success){
                LightFields();
                alert("Пользователь с таким именем уже существует!")
                console.log(json)
            }
        }
        else {
            console.log(typeof(new_user))
            console.log(new_user)
        }
    } catch (error) {
        console.error('Ошибка', error);
    }
}

//очитска полей ввода после отправки формы
function ClearField(){
    const inputs = Array.from(RegForm.querySelectorAll(".input_field"))
    inputs.forEach(input => {
        input.value = ""
    });
}   

//удаление пробелов
function deletSpace() {
    loginField.value= loginField.value.replace(/\s/, "");
    emailField.value= emailField.value.replace(/\s/, "");
    passwordField.value = passwordField.value.replace(/\s/, "");
}

function LightFields() {
    if (reg_login.test(loginField.value) == true){
        loginField.classList.add("green_shadow");
        loginField.classList.remove("red_shadow");
        loginStatus.innerHTML = "&#10003;";
        loginStatus.style.color = "#00ff04";
} else if (reg_login.test(loginField.value) != true){
        loginField.classList.remove("green_shadow");
        loginField.classList.add("red_shadow");
        loginStatus.innerHTML = "&#10006;";
        loginStatus.style.color = "red";
}  
if (reg_pass.test(passwordField.value) == true){
        passwordField.classList.add("green_shadow");
        passwordField.classList.remove("red_shadow");
        passwordStatus.innerHTML = "&#10003;";
        passwordStatus.style.color = "#00ff04";
} else if (reg_pass.test(passwordField.value) != true) {
        passwordField.classList.remove("green_shadow");
        passwordField.classList.add("red_shadow");
        passwordStatus.innerHTML = "&#10006;";
        passwordStatus.style.color = "red";
}
if (reg_email.test(emailField.value) == true){
    emailField.classList.add("green_shadow");
    emailField.classList.remove("red_shadow");
    emailStatus.innerHTML = "&#10003;";
    emailStatus.style.color = "#00ff04";
} else if (reg_email.test(emailField.value) != true) {
    emailField.classList.remove("green_shadow");
    emailField.classList.add("red_shadow");
    emailStatus.innerHTML = "&#10006;";
    emailStatus.style.color = "red";
}
}