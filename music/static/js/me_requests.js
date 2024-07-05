document.addEventListener('DOMContentLoaded', ()=>{
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
    const accept_list = document.querySelectorAll('#accept')
    const reject_list = document.querySelectorAll('#reject')

    function manage(element, action){

         let idItem = element.parentNode.parentNode.querySelector('input').value
            console.log(idItem)
            fetch('/music/fmanageRequests/',{
            method: 'POST',
            credentials: 'same-origin',
            headers:{
                 'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({'action': action, 'id': idItem})

        })
            .then(response => response.json())
            .then(data => {

            window.location.href = '/musicexchange'

            })

    }


    accept_list.forEach((element) =>{

        element.addEventListener('click', () => {
            console.log(element)
            manage(element, 'accept')
        })
    })

    reject_list.forEach((element) =>{

        element.addEventListener('click', () => {
            console.log(element)
            manage(element, 'reject')
        })
    })


})