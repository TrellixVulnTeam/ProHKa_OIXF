import jwt_decode from "jwt-decode";

import Swal from 'sweetalert2'
const Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
    didOpen: (toast) => {
        toast.addEventListener('mouseenter', Swal.stopTimer)
        toast.addEventListener('mouseleave', Swal.resumeTimer)
    }
})


export function getCookie(name) {
    let value = "; " + document.cookie;
    let parts = value.split("; " + name + "=");
    if (parts.length == 2)
        return parts.pop().split(";").shift();
}



export function showError(error: any, status: any, table: string[], allErrors: any) {
    if (error && status == 400) {
        table = allErrors
        // return table
    }
    else if (status == 500) {
        SwallModal('error', 'Erreur', "Veuillez contacter l'administrateur")
    }
}


export function SwallModal(icons: any, title: string, message: string) {
    Swal.fire({
        icon: icons,
        title: title,
        text: message,
        // footer: '<a href="">Why do I have this issue?</a>'
    })
}


export function toastShow(icon: any, message: string) {
    Toast.fire({
        icon: icon,
        title: message
    })
}



export function foundToken(securityObject: any) {
    var token = localStorage.getItem('currentUser')
    if (token) {
        securityObject = jwt_decode(token)
        if (securityObject["key"] == "archiSoftware") {
            return securityObject
        }
        else {
            return null
        }
    }
    else {
        return null
    }
}



export const genders = ["Masculin", "Feminin"]
