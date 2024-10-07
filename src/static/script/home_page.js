const btnLike = document.querySelector(".like");
const btnCreatePost = document.querySelector(".create_post");
const btnDeletePost = document.querySelector(".delete_post");
const btnLogout = document.querySelector(".logout");
const btnModify = document.querySelector(".modify_post");

btnCreatePost.addEventListener("click", create_post);
btnLogout.addEventListener("click", logout);


document.addEventListener("click", e=>{
    if (e.target.classList.contains("like")) {
        like_post(e.target.id);
    }
})

document.addEventListener("click", e=>{
    if (e.target.classList.contains("delete_post")) {
        delete_post(e.target.id);
    }
})

document.addEventListener("click", e=>{
    if (e.target.classList.contains("modify_post")) {
        replace_div(e.target.id);
        Array.from(document.querySelectorAll(".btn")).forEach(element => {
            element.setAttribute("disabled", "true");
        });
    }
    

})

document.addEventListener("click", e=>{
    if (e.target.classList.contains("cancel_changes")) {
        window.location.href = "http://127.0.0.1:8093/pages/home_page";
    }
})

document.addEventListener("click", e=>{
    if (e.target.classList.contains("accept_changes")) {
        const text = document.querySelector("[data-text-id=" + CSS.escape(e.target.id) + "]")
       modify_post(e.target.id, text.value);
    }
})

async function logout() {
    try {
        const response = await fetch("http://127.0.0.1:8093/auth/logout", {
            method: "POST",
            });
            if(response.ok) {
                const json = await response.json();
                if (json.success) {
                    window.location.href = "http://127.0.0.1:8093/pages/authenticate"
                    console.log(json);
                    
                }
                else if (!json.success){
                    console.log(json)
                }
            }
    } catch (error) {
        
    }
}

async function create_post() {
    window.location.href = "http://127.0.0.1:8093/pages/create_post_window"
}

async function delete_post(id) {
    try {
        const response = await fetch(`http://127.0.0.1:8093/profile/delete_post/?post_id=${id}`, {
            method: "DELETE",
            });
            if(response.ok) {
                const json = await response.json();
                if (json.success) {
                    window.location.href = "http://127.0.0.1:8093/pages/home_page"
                    console.log(json);
                    
                }
                else if (!json.success){
                    console.log(json)
                }
            }
    } catch (error) {
        
    }
}

async function like_post(id) {
    const likeCount = document.querySelector("[data-id=" + CSS.escape(id) + "]");
    try {
        const response = await fetch(`http://127.0.0.1:8093/profile/like_post?post_id=${id}`, {
            method: "PATCH",
            });
            if(response.ok) {
                const json = await response.json();
                if (json.success && json.mes == 'like') {
                    likeCount.innerHTML=parseInt(likeCount.innerHTML)+1;
                    console.log(json);
                    
                }
                else if(json.success && json.mes == 'dislike'){
                    likeCount.innerHTML=parseInt(likeCount.innerHTML)-1;
                    console.log(json);
                }
                else if (!json.success){
                    console.log(json)
                }
            }
    } catch (error) {
        
    }
}

async function modify_post(id, text) {
    console.log(text)
    const new_post_data ={
        post_id: id,
        new_text: text
    }
        try {
            let response = await fetch("http://127.0.0.1:8093/profile/modify_post/", {
                method: "PATCH",
                body: JSON.stringify(new_post_data),
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
                    window.location.href = "http://127.0.0.1:8093/pages/home_page";
                }
                else if (!json.success){
                    console.log(json);
                }
            } 
        } catch (error) {
            
        }
}


function replace_div(id) {
    const modifed_post = document.querySelector("[data-post-id=" + CSS.escape(id) + "]");
    const modifed_text = document.querySelector("[data-text-id=" + CSS.escape(id) + "]");
    const btn_mod = document.querySelector("[data-mod-id=" + CSS.escape(id) + "]");
    const del_and_mod = document.querySelector("[data-mod_and_del-id=" + CSS.escape(id) + "]");

   
    const btn_cancel = del_and_mod.insertBefore(document.createElement('button'), btn_mod);
    const btn_accept = del_and_mod.insertBefore(document.createElement('button'), btn_cancel);


    btn_accept.innerHTML = "&#10004;";
    btn_accept.classList.add("accept_changes");
    btn_accept.setAttribute("id", id)
    
    btn_cancel.innerHTML = "&#10006;";
    btn_cancel.classList.add("cancel_changes");

    const textarea = document.body.appendChild(document.createElement('textarea'));
    textarea.setAttribute("rows", "15");
    textarea.setAttribute("cols", "85");
    textarea.setAttribute("data-text-id", id);
    
    textarea.innerHTML = modifed_text.innerHTML.trim();
    modifed_text.parentNode.replaceChild(textarea, modifed_text);

}

