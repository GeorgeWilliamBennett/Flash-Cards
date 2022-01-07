const textField = document.getElementById('set-name')
const errorMessage = document.getElementById('error')
const form = document.getElementById('create-set-form')

function empty () {
    textField.backgroundColor = 'pink'
    errorMessage.innerHTML - 'Name can not be empty'
}

function invalidDigit () {
    textField.style.backgroundColor = 'pink'
    errorMessage.innerHTML = 'Set names must begin with a letter'
}

function invalidSpecial() {
    textField.style.backgroundColor = 'pink'
    errorMessage.innerHTML = 'Set names can not have special characters'
}

form.addEventListener('submit', (e)=> {
    const startsWithDigit = /^[a-zA-Z\s]/.test(textField.value)
    const containsSpecial = /^[a-zA-Z0-9\s]*$/.test(textField.value)
    if (textField.length < 1){
        e.preventDefault()
        empty()
    } else if (!startsWithDigit) {
        e.preventDefault();
        invalidDigit();
    } else if (!containsSpecial) {
        e.preventDefault();
        invalidSpecial();
    }
    return false
})


