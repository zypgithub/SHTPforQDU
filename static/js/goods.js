function checkAnswer(){
    var response = document.getElementById('answer').value;
    if (response == "correctanswer")
        location = 'right.html';
    else
        location = 'wrong.html';
    return false;
}
