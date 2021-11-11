$(document).ready(function(){
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    csrftoken = getCookie('csrftoken')

    $("#submitMsg").click(function(e){
        e.preventDefault()

        let formData = new FormData();
        formData.append("name", $("#nameMsg").val())
        formData.append("email", $("#emailMsg").val())
        formData.append("phone", $("#phoneMsg").val())
        formData.append("subject", $("#subjectMsg").val())
        formData.append("message", $("#messageMsg").val())
        $.ajax({
            method:"POST",
            url:"/custom/api/contact-us/",
            processData:false,
            contentType:false,
            mimeType:"multipart/form-data",
            headers:{
            "X-CSRFToken": csrftoken
            },
            data:formData,
            success:function(res){
                alert("Message envoyé")
                document.getElementById("contactForm").reset()
                document.getElementById("nameMsg").classList.remove("is-valid")
                document.getElementById("nameMsg").classList.remove("is-invalid")
                document.getElementById("emailMsg").classList.remove("is-valid")
                document.getElementById("emailMsg").classList.remove("is-invalid")
                document.getElementById("phoneMsg").classList.remove("is-valid")
                document.getElementById("phoneMsg").classList.remove("is-invalid")
                document.getElementById("subjectMsg").classList.remove("is-valid")
                document.getElementById("subjectMsg").classList.remove("is-invalid")
                document.getElementById("messageMsg").classList.remove("is-valid")
                document.getElementById("messageMsg").classList.remove("is-invalid")
                document.getElementById("nameErr1").textContent=errors['name']
                document.getElementById("emailErr1").textContent=errors['email']
                document.getElementById("phoneErr1").textContent=errors['phone']
                document.getElementById("objectErr1").textContent=errors['subject']
                document.getElementById("messageErr1").textContent=errors['message']
            },
            error:function(err){
                errors = JSON.parse(err.responseText)
                if (err.status === 400 && errors) {
                    let keysErrors = Object.keys(errors)
                    for(let key in keysErrors){
                        if (keysErrors[key] == 'name') {
                            document.getElementById("nameMsg").classList.add("is-invalid")
                            document.getElementById("nameErr1").textContent=errors['name']
                        }
                        if (keysErrors[key] == 'email') {
                            document.getElementById("emailMsg").classList.add("is-invalid")
                            document.getElementById("emailErr1").textContent=errors['email']
                        }
                        if (keysErrors[key] == 'phone') {
                            document.getElementById("phoneMsg").classList.add("is-invalid")
                            document.getElementById("phoneErr1").textContent=errors['phone']
                        }
                        if (keysErrors[key] == 'subject') {
                            document.getElementById("subjectMsg").classList.add("is-invalid")
                            document.getElementById("objectErr1").textContent=errors['subject']
                        }
                        if (keysErrors[key] == 'message') {
                            document.getElementById("messageMsg").classList.add("is-invalid")
                            document.getElementById("messageErr1").textContent=errors['message']
                        }
                    }
                    if (errors.hasOwnProperty("name") == false) {
                        document.getElementById("nameMsg").classList.remove("is-invalid")
                        document.getElementById("nameMsg").classList.add("is-valid")
                        document.getElementById("nameErr1").textContent=''
                    }
                    if (errors.hasOwnProperty("email") == false) {
                        document.getElementById("emailMsg").classList.remove("is-invalid")
                        document.getElementById("emailMsg").classList.add("is-valid")
                        document.getElementById("emailErr1").textContent=''
                    }
                    if (errors.hasOwnProperty("phone") == false) {
                        document.getElementById("phoneMsg").classList.remove("is-invalid")
                        document.getElementById("phoneMsg").classList.add("is-valid")
                        document.getElementById("phoneErr1").textContent=''
                    }
                    if (errors.hasOwnProperty("subject") == false) {
                        document.getElementById("subjectMsg").classList.remove("is-invalid")
                        document.getElementById("subjectMsg").classList.add("is-valid")
                        document.getElementById("objectErr1").textContent=''
                    }
                    if (errors.hasOwnProperty("message") == false) {
                        document.getElementById("messageMsg").classList.remove("is-invalid")
                        document.getElementById("messageMsg").classList.add("is-valid")
                        document.getElementById("messageErr1").textContent=''
                    }
                    
                }
            }
        })
    })
})