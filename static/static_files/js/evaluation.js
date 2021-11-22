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
        getIdInput.classList?.add("is-invalid")
        getIdError.textContent=textError
      }
      if (tableError.hasOwnProperty(name) == false) {
        getIdInput?.classList?.remove("is-invalid")
        getIdInput?.classList?.add("is-valid")
        getIdError?.textContent=''
      }
}

function revomeError(elmntId, errorId){
    elmntId.classList?.remove("is-invalid")
    elmntId.classList?.remove("is-valid")
    errorId.textContent=''
}


var csrftoken = getCookie('csrftoken');



$(document).ready(function(){
    $("#lauchModal10").click(function(e){
        document.getElementById("formSubmitRegister10").reset()
        revomeError(document.getElementById("inputNote0"), document.getElementById("showErrorPunctuality01"))
        revomeError(document.getElementById("inputNote1"), document.getElementById("showErrorAdaptation01"))
        revomeError(document.getElementById("inputNote2"), document.getElementById("showErrorRespect01"))
        revomeError(document.getElementById("inputNote3"), document.getElementById("showErrorIniative01"))
        revomeError(document.getElementById("inputNote"), document.getElementById("showErrorFinalNote01"))
        revomeError(document.getElementById("inputComment12"), document.getElementById("showErrorComment01"))
        revomeError('', document.getElementById("showErrorDecision01"))

        let employe = $('[id^=idForName12-]')[0].textContent
        let idProfile = $('[id^=idForName12-]')[0].getAttribute('id')
        document.getElementById("inputWorker41").value = idProfile
        document.getElementById("inputWorker4").value = employe
    })
    
    var input1 = document.getElementById("inputNote0")
    var input2 = document.getElementById("inputNote1")
    var input3 = document.getElementById("inputNote2")
    var input4 = document.getElementById("inputNote3")

    input1.addEventListener('keyup', function(e){
        getTotal()
        
    })
    input2.addEventListener('keyup', function(e){
        getTotal()
        
    })
    input3.addEventListener('keyup', function(e){
        getTotal()
        
    })
    input4.addEventListener('keyup', function(e){
        getTotal()
        
    })
    function getTotal(){
        var arr = document.querySelectorAll('.input-field')
        var total = 0;
        for(var i=0; i<arr.length; i++){
        if(parseInt(arr[i].value)){
            if(parseInt(arr[i].value) > 5 || parseInt(arr[i].value) < 0){
                arr[i].classList.add("is-invalid")
                alert("Les notes sont comprises entre 1 et 5")
            }
            else{
                total += parseInt(arr[i].value)
            }
        }
        document.getElementById('inputNote').value = total
        }
    };
    

    $("#sendNote12").click(function(e){
        let radioButton = document.getElementsByName("inlineRadioOptions");
        let profileId = document.getElementById('inputWorker41').value.split('-').pop()
        let agreeOrNot = '';
        for(i=0; i<radioButton.length; i++){
            if(radioButton[i].checked){
                agreeOrNot = radioButton[i].value
            }
        }
        e.preventDefault();
        let formData = new FormData();
        formData.append("punctuality", document.getElementById('inputNote0').value)
        formData.append("adaptation", document.getElementById('inputNote1').value)
        formData.append("respect", document.getElementById('inputNote2').value)
        formData.append("iniative", document.getElementById('inputNote3').value)
        formData.append("finalNote", document.getElementById('inputNote').value)
        formData.append("comment", document.getElementById('inputComment12').value)
        formData.append("userId", document.getElementById('inputName43').value)
        formData.append("profileUser", profileId)
        formData.append("trueRadio", agreeOrNot)
        // formData.append("falseRadio", document.getElementById('inlineRadio2').value)

        $.ajax({
            method:"POST",
            url:"/custom/api/add-evaluation/",
            processData:false,
            contentType:false,
            mimeType:"multipart/form-data",
            headers:{
            "X-CSRFToken": csrftoken
            },
            data:formData,
            success:function(res){
                if(res){
                    console.log("the user register ", res)
                    $('#exampleModal120').modal('hide');
                    alert("Avis enregistré avec succès")
                }
            },
            error:function(err){
                let errors = JSON.parse(err.responseText)
                if (err.status === 400 && errors){
                    let keysErrors = Object.keys(errors)
                    for(let key in keysErrors){
                        setError(keysErrors[key], 'punctuality', errors, document.getElementById("inputNote0"), errors['punctuality'], document.getElementById("showErrorPunctuality01"))
                        setError(keysErrors[key], 'adaptation', errors, document.getElementById("inputNote1"), errors['adaptation'], document.getElementById("showErrorAdaptation01"))
                        setError(keysErrors[key], 'respect', errors, document.getElementById("inputNote2"), errors['respect'], document.getElementById("showErrorRespect01"))
                        setError(keysErrors[key], 'iniative', errors, document.getElementById("inputNote3"), errors['iniative'], document.getElementById("showErrorIniative01"))
                        setError(keysErrors[key], 'finalNote', errors, document.getElementById("inputNote"), errors['finalNote'], document.getElementById("showErrorFinalNote01"))
                        setError(keysErrors[key], 'comment', errors, document.getElementById("inputComment12"), errors['comment'], document.getElementById("showErrorComment01"))
                        setError(keysErrors[key], 'decision', errors, '', errors['decision'], document.getElementById("showErrorDecision01"))
                    }
                }
            }
        })
    })
})