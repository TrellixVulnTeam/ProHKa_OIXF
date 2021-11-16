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

function setError(key, name, tableError, getIdInput, textError, getIdError){
    if (key == name) {
        getIdInput.classList.add("is-invalid")
        getIdError.textContent=textError
      }
      if (tableError.hasOwnProperty(name) == false) {
        getIdInput.classList.remove("is-invalid")
        getIdInput.classList.add("is-valid")
        getIdError.textContent=''
      }
}

function revomeError(elmntId, errorId){
    elmntId.classList.remove("is-invalid")
    elmntId.classList.remove("is-valid")
    errorId.textContent=''
}


var csrftoken = getCookie('csrftoken');

$(document).ready(function(){
    $("#modalRegister01").click(function(e){
        document.getElementById("formSubmitRegister").reset()
        revomeError(document.getElementById("inputName4"), document.getElementById("showErrorName01"))
        revomeError(document.getElementById("inputSurname10"), document.getElementById("showErrorSurname01"))
        revomeError(document.getElementById("inputEmail4"), document.getElementById("showErrorEmail01"))
        revomeError(document.getElementById("inputPassword4"), document.getElementById("showErrorPassword01"))
        revomeError(document.getElementById("inputPassword41"), document.getElementById("showErrorPassword02"))
        revomeError(document.getElementById("inputTel2"), document.getElementById("showErrorPhone"))
        revomeError(document.getElementById("inputCity12"), document.getElementById("showErrorCity01"))
    })
   
    // *********************** REGISTER USER **************************
    $("#registerUser12").click(function(e){
        e.preventDefault();
        let formData = new FormData();
        formData.append("name", document.getElementById('inputName4').value)
        formData.append("surname", document.getElementById('inputSurname10').value)
        formData.append("email", document.getElementById('inputEmail4').value)
        formData.append("password1", document.getElementById('inputPassword4').value)
        formData.append("password2", document.getElementById('inputPassword41').value)
        formData.append("phone", document.getElementById('inputTel2').value)
        formData.append("cityLive", document.getElementById('inputCity12').value)
        formData.append("typeUser", document.getElementById('typeUser').value)

        $.ajax({
            method:"POST",
            url:"/auth/api/register/",
            processData:false,
            contentType:false,
            mimeType:"multipart/form-data",
            headers:{
            "X-CSRFToken": csrftoken
            },
            data:formData,
            success:function(res){
                console.log("the user register ", res)
                if(JSON.parse(res)["data"] ==="success"){
                    document.getElementById("formSubmitRegister").reset()
                    $('#exampleModal-register').modal('hide');
                }
            },
            error:function(err){
                let errors = JSON.parse(err.responseText)
                if (err.status === 400 && errors){
                    let keysErrors = Object.keys(errors)
                    for(let key in keysErrors){
                        setError(keysErrors[key], 'name', errors, document.getElementById("inputName4"), errors['name'], document.getElementById("showErrorName01"))
                        setError(keysErrors[key], 'surname', errors, document.getElementById("inputSurname10"), errors['suname'], document.getElementById("showErrorSurname01"))
                        setError(keysErrors[key], 'email', errors, document.getElementById("inputEmail4"), errors['email'], document.getElementById("showErrorEmail01"))
                        setError(keysErrors[key], 'password1', errors, document.getElementById("inputPassword4"), errors['password1'], document.getElementById("showErrorPassword01"))
                        setError(keysErrors[key], 'password2', errors, document.getElementById("inputPassword41"), errors['password2'], document.getElementById("showErrorPassword02"))
                        setError(keysErrors[key], 'phone', errors, document.getElementById("inputTel2"), errors['phone'], document.getElementById("showErrorPhone"))
                        setError(keysErrors[key], 'cityLive', errors, document.getElementById("inputCity12"), errors['cityLive'], document.getElementById("showErrorCity01"))
                    }
                }
            }
        })
    })

    $("#selectProfile10").click(function(e){
        e.preventDefault()
        let formData = new FormData();
        formData.append("idProfile", document.getElementById('profileSelected12').value)
        $.ajax({
            method:"POST",
            url:"/custom/api/choice-client/",
            processData:false,
            contentType:false,
            mimeType:"multipart/form-data",
            headers:{
            "X-CSRFToken": csrftoken
            },
            data:formData,
            success:function(res){
                if (res) {
                    alert("Profil selectionne merci de nous faire confiance")
                    window.location="/"
                }
            },
            error:function(err){
                // console.log("the error register ", err)
            }
        })
    })
})