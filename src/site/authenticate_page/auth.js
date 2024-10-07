const btnAuth = document.querySelector(".auth_btn");
const btnReg = document.querySelector(".reg_btn");
const user_login = document.querySelector('[name="username"]');
const user_pass = document.querySelector('[name="password"]');
const auth_form = document.querySelector(".auth_form");

// const digit = /[0-9]/;
// const lowerCase = /[a-z]/;
// const upperCase = /[A-Z]/;
// const symb = /(?!.*&)[a-zA-Z0-9]+/
// console .log([digit, lowerCase, upperCase, symb].every((re) => re.test("f2f&F")))

const reg_login = /.{3,16}/;
const reg_pass = /.{8,30}/;


auth_form.addEventListener("input", ValidateForm)
btnAuth.addEventListener("click", Authorization);
//проверка на количество символов в полях ввода
function ValidateForm() {
    deletSpace();
    if (reg_pass.test(user_pass.value)==true && reg_login.test(user_login.value)==true){
        btnAuth.removeAttribute("disabled");
    } else {
        btnAuth.setAttribute("disabled", "true");
    }

}
//переход на страницу регистрации
btnReg.addEventListener("click", function(){
    window.location.replace("http://127.0.0.1:5500/src/site/registration_page/registration_page.html");
})


//отправка запроса на вход
async function Authorization() {
    const formData = new FormData(auth_form);
    const data = Object.fromEntries(formData.entries())
    // const User = {
    //     username : user_login.value,
    //     password: user_pass.value,
    //     grant_type: "password"
    // }
    // ждем ответ с сервера
    try {
        let response = await fetch("http://localhost:8087/auth/login/", {
            method: "POST",
            body: new URLSearchParams(data),
            headers: { //необходимые заголовки из документации API 
                // 'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        });
        // если с ответом все ОК, то получаем из него JSON
        if(response.ok) {
            const json = await response.json();
            if (json.success) {
                console.log(json);
                const home_page = await fetch("http://localhost:8087/pages/home_page");
                console.log(home_page)
            }
            else if (!json.success){
                ClearField();
                console.log(json);
                alert("Проверьте правильность ввода логина и пароля!");
            }
        } 
    } catch (error) {
        
    }
}
//очиcтка полей ввода
function ClearField(){
    const inputs = Array.from(auth_form.querySelectorAll(".input_field"))
    inputs.forEach(input => {
        input.value = ""
    });
}   
//Удаление пробелов при вводе
function deletSpace() {
    user_login.value= user_login.value.replace(/\s/, "");
    user_pass.value = user_pass.value.replace(/\s/, "");
}
//остановка отправки формы
auth_form.addEventListener('submit', function (e) {
    e.preventDefault();
})