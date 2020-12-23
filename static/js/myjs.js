function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

chkQuestion = document.getElementById(
                "question-form").addEventListener('click', validateAnswer)
            
function validateAnswer(e){
    let selectData = e.explicitOriginalTarget.nextElementSibling.textContent;
    selectData = selectData.trim();
    let objectId = e.explicitOriginalTarget.nextElementSibling.classList[1];

    var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance 
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            let qnaApiResponse = JSON.parse(this.responseText);
            // console.log(qnaApiResponse);
            console.log(objectId);
                var xmlhttp1 = new XMLHttpRequest();   // new HttpRequest instance 

                xmlhttp1.open("PUT", `/api/question/${Number(objectId)}`);
                xmlhttp1.setRequestHeader('Content-type','application/json; charset=utf-8');
                xmlhttp1.setRequestHeader('X-CSRFToken', csrftoken);
                xmlhttp1.send(JSON.stringify({
                    correct_answer: qnaApiResponse.correct_answer,
                    options: qnaApiResponse.options,
                    clicked: 1,
                    click_data: selectData,
                }));
                if (selectData == qnaApiResponse.correct_answer){
                let removeOption = document.getElementsByClassName('form-check');
                for (let i=0; i < removeOption.length; i++){
                    if (removeOption[i].textContent.trim() == selectData){
                        removeOption[i].firstElementChild.style.background = 'green';
                        removeOption[i].firstElementChild.setAttribute('disabled', '');
                    } else {
                        removeOption[i].firstElementChild.setAttribute('disabled', '');
                    };
                };
            } else {
                let removeOption = document.getElementsByClassName('form-check');
                for (let i=0; i < removeOption.length; i++){
                    if (removeOption[i].textContent.trim() == selectData){
                        removeOption[i].firstElementChild.style.background = 'red';
                        removeOption[i].firstElementChild.setAttribute('disabled', '');
                    } else {
                        if (removeOption[i].textContent.trim() == qnaApiResponse.correct_answer){
                            removeOption[i].firstElementChild.style.background = 'green';
                            removeOption[i].firstElementChild.setAttribute('disabled', '');
                        } else{
                            removeOption[i].firstElementChild.setAttribute('disabled', '');
                        }
                    };
                }
            };
        };
    };

    xmlhttp.open("GET", `/api/question/${objectId}`);
    xmlhttp.setRequestHeader('X-CSRFToken', csrftoken);
    xmlhttp.send();
}
