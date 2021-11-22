
$(document).ready(function(){
    function setError(key, name, tableError, getIdInput, textError, getIdError){
        if (key == name) {
            getIdInput?.classList?.add("is-invalid")
            getIdError.textContent=textError
          }
          if (tableError.hasOwnProperty(name) == false) {
            getIdInput?.classList?.remove("is-invalid")
            getIdInput?.classList?.add("is-valid")
            getIdError.textContent=''
          }
    }

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
    function retrieveCurrentUser(){
        var currentUser = document.getElementById("retriveUser").value
        return currentUser
    }

    
    
    $("#submitMsg").click(function(e){
        e.preventDefault()

        let formData = new FormData();
        let formDataAnonymous = new FormData();
        if (retrieveCurrentUser() == 'AnonymousUser') {
            formDataAnonymous.append("name", $("#nameMsg").val())
            formDataAnonymous.append("email", $("#emailMsg").val())
            formDataAnonymous.append("phone", $("#phoneMsg").val())
            formDataAnonymous.append("subject", $("#subjectMsg").val())
            formDataAnonymous.append("message", $("#messageMsg").val())
            $.ajax({
                method:"POST",
                url:"/custom/api/contact-us/",
                processData:false,
                contentType:false,
                mimeType:"multipart/form-data",
                headers:{
                "X-CSRFToken": csrftoken
                },
                
                data:formDataAnonymous,
                success:function(res){
                    alert("Messagee envoyé")
                    window.location.reload()
                },
                error:function(err){
                    errors = JSON.parse(err.responseText)
                    if (err.status === 400 && errors) {
                        let keysErrors = Object.keys(errors)
                        for(let key in keysErrors){
                            setError(keysErrors[key], 'name', errors, document.getElementById("nameMsg"), errors['name'], document.getElementById("nameErr1"))
                            setError(keysErrors[key], 'email', errors, document.getElementById("emailMsg"), errors['email'], document.getElementById("emailErr1"))
                            setError(keysErrors[key], 'phone', errors, document.getElementById("phoneMsg"), errors['phone'], document.getElementById("phoneErr1"))
                            setError(keysErrors[key], 'subject', errors, document.getElementById("subjectMsg"), errors['subject'], document.getElementById("objectErr1"))
                            setError(keysErrors[key], 'message', errors, document.getElementById("messageMsg"), errors['subject'], document.getElementById("messageErr1"))
                        }
                    }
                }
            })
        }
        else{
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
                    alert("Messagee envoyé")
                    window.location.reload()
                },
                error:function(err){
                    errors = JSON.parse(err.responseText)
                    if (err.status === 400 && errors) {
                        let keysErrors = Object.keys(errors)
                        for(let key in keysErrors){
                            setError(keysErrors[key], 'subject', errors, document.getElementById("subjectMsg"), errors['subject'], document.getElementById("objectErr1"))
                            setError(keysErrors[key], 'message', errors, document.getElementById("messageMsg"), errors['subject'], document.getElementById("messageErr1"))
                        }
                    }
                }
            })
        }
    })
})