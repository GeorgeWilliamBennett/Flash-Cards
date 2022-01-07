function show_answer() {
    document.getElementById('your-answer').style.display = 'none'
    document.getElementById('your-answer-final').style.display = 'block'
    document.getElementById('your-answer-final').innerHTML =
        document.getElementById('your-answer').value
    document.getElementById('answer-div').style.display = 'block'
    document.getElementById('confirm-answer').style.display = 'none'
    return false}   
    
    
document.getElementById('confirm-answer').addEventListener('click', show_answer)

document.getElementById('delete-card').
addEventListener('click', () => {
  confirm("Are you sure you want to delete this card?")
})