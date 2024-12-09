const btnCloseModal = document.querySelector(".close_window");
const btnClearField = document.querySelector(".clear_field");
const btnPublishPost = document.querySelector(".publish");

const postTheme = document.querySelector('[name="post_theme"]');
const postText = document.querySelector('[name="post_text"]');

const createForm = document.querySelector(".creation_form");


createForm.addEventListener("submit", e=>{
    e.preventDefault();
});

btnCloseModal.addEventListener("click", function(){
    window.location.href = "http://127.0.0.1:8150/pages/home_page";
});

btnPublishPost.addEventListener("click", CreatePost)
btnClearField.addEventListener("click", ClearField)


async function CreatePost() {
        const post_data ={
            article_theme: postTheme.value,
            article_text: postText.value
        }
    try {
        let response = await fetch("http://127.0.0.1:8150/profile/create_post/", {
            method: "POST",
            body: JSON.stringify(post_data),
            headers: { //необходимые заголовки из документации API 
                // 'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        });
        // если с ответом все ОК, то получаем из него JSON
        if(response.ok) {
            const json = await response.json();
            if (json.success) {
                console.log(json);
                window.location.href = "http://127.0.0.1:8150/pages/home_page";
            }
            else if (!json.success){
                console.log(json);
            }
        } 
    } catch (error) {
        
    }
}

function ClearField(){
    postText.value = ""
}   