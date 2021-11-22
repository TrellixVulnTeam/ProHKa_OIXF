export function revomeError(elmntId, errorId){
    elmntId.classList?.remove("is-invalid")
    elmntId.classList?.remove("is-valid")
    errorId.textContent=''
}

export function setError(key, name, tableError, getIdInput, textError, getIdError){
    if (key == name) {
        getIdInput?.classList.add("is-invalid")
        getIdError?.textContent=textError
      }
      if (tableError.hasOwnProperty(name) == false) {
        getIdInput?.classList?.remove("is-invalid")
        getIdInput?.classList?.add("is-valid")
        getIdError?.textContent=''
      }
}