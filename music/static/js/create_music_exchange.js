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



const username = document.querySelector('#usernameq');
const search = document.querySelector('#search');

const itemSelected = document.querySelector('#itemSelected')
const table = document.querySelector('#table')

    let itemToSend = document.querySelector('#itemtosend')
    let Send = document.querySelector('#send')
    let Delete = document.querySelector('#delete')

function truncateString(str) {
    if (str.length > 40) {
        return str.substring(0, 37) + '...';
    }
    return str;
}


function elementRenderize(element, item){
        let divRow = document.createElement('div');
    divRow.classList.add('row');

    let divImg = document.createElement('div');
    divImg.classList.add('img');
    let aImg = document.createElement('a');
    aImg.href = element.external_urls.spotify;
    aImg.setAttribute('target', '_blank')


    let imgA = document.createElement('img');
    imgA.classList.add('cover-img');
    if (item === 'track')
    {
    imgA.setAttribute('src', element.album.images[0].url);
    }
    else{

    imgA.setAttribute('src', element.images[0].url);
    }





    let divLike = document.createElement('div');
    divLike.classList.add('like-icon');

    let btnLike = document.createElement('button');
    btnLike.setAttribute('id', 'select')
    btnLike.classList.add('select')
    btnLike.textContent = 'Select';

    let divSongTitle = document.createElement('div');
    divSongTitle.classList.add('song-title');

    let aSongTitle = document.createElement('a');
    aSongTitle.classList.add('text-link-main', 'primary-fs');
    aSongTitle.setAttribute('target', '_blank')
    aSongTitle.href = element.external_urls.spotify;
    aSongTitle.textContent = truncateString(element.name);


    let divArtistName = document.createElement('div');
    divArtistName.classList.add('song-title');

    let aArtistName = document.createElement('a');
    aArtistName.classList.add('text-link-main', 'secondary-fs');
    aArtistName.href = element.external_urls.spotify;
    aArtistName.setAttribute('target', '_blank')
    if (item === 'playlist'){
        aArtistName.textContent = truncateString(element.owner.display_name);
    }
    else{
        aArtistName.textContent = truncateString(element.artists[0].name);
    }


    let divTimeAgo = document.createElement('div');
    //let date = element.count;
    divTimeAgo.textContent = element.type;

    let divId = document.createElement('div')
    divId.classList.id='itemId'
    let inputH = document.createElement('input')
    inputH.setAttribute('type', 'hidden')
    inputH.value = element.id

    divId.appendChild(inputH)

    divSongTitle.appendChild(aSongTitle);
    aImg.appendChild(imgA);
    divImg.appendChild(aImg);
    divLike.appendChild(btnLike);
    divArtistName.appendChild(aArtistName);


    divRow.appendChild(divImg);
    divRow.appendChild(divSongTitle);
    divRow.appendChild(divArtistName);
    divRow.appendChild(divTimeAgo);
    divRow.appendChild(divLike)
    divRow.appendChild(divId)

    table.appendChild(divRow);


    btnLike.addEventListener('click', () => {

        let element = btnLike.parentNode.parentNode
        console.log(element)

        let clonedElement = element.cloneNode('true')

        let textReference = document.querySelector('#textReference')

        let h4 = document.createElement('h4')
        h4.textContent = 'Selected:'

        itemToSend.innerHTML = ''
        itemToSend.appendChild(h4)
        itemToSend.appendChild(clonedElement)
        textReference.scrollIntoView({
            behavior: 'smooth',

        })


    })



}

    let timeout = null;


username.addEventListener('input', () =>{
    clearTimeout(timeout)

    timeout = setTimeout(() => {
        fetch('/music/fusername/',{
            method: 'POST',
            credentials: 'same-origin',
            headers:{
                 'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({'username':username.value})

        })
        .then(response => response.json())
        .then(data=> {
            console.log(data)
            let textIncorrect = document.querySelector('#text-incorrect')
            if (data.user_exists === true)
            {
                username.classList.remove('incorrect')
                textIncorrect.textContent = ''
                username.setAttribute('isvalid', 'True')


            }
            else{


                textIncorrect.innerHTML ="This user doesn't exists"
                if (username.classList.contains('incorrect') === false)
                {
                    username.classList.add('incorrect')
                    username.setAttribute('isvalid', 'False')


                }

            }
        })
    },550)




})


search.addEventListener('input', () =>{

    clearTimeout(timeout);

    if (search.value.length > 0 ) {
        table.innerHTML = ''
        timeout = setTimeout(() => {
            fetch('/music/fsearch/', {
                method: 'POST',
                credentials: 'same-origin',
                headers: {
                    'Accept': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({'search': search.value})

            })
                .then(response => response.json())
                .then(data => {
                    console.log(data)

                    data.results.albums.items.forEach((result) => elementRenderize(result, 'album'))
                    data.results.playlists.items.forEach((result) => elementRenderize(result, 'playlist'))
                    data.results.tracks.items.forEach((result) => elementRenderize(result, 'track'))
                        //song_renderize(result)



                })

        }, 750)


    }






})

    Send.addEventListener('click', () =>{
        let divText = document.querySelector('#second-text-incorrect')


        console.log('send')
        console.log(itemToSend.children.length)
        console.log(itemToSend)


        if (itemToSend.children.length < 2)
        {

            divText.textContent = 'Must provide an item to share'
        }
        else if( username.classList.contains('incorrect') ){
            divText.textContent = 'Invalid username'

        }
        else
        {
            divText.textContent = ''
            let item = itemToSend.querySelector('.row')
            console.log(item)

            let type = item.childNodes[3].textContent
            let id = item.querySelector('input').value

            console.log(type, id)


            Send.setAttribute('disabled', '')

            let advice = document.createElement('h3')
            advice.textContent = 'Your request is being created'
            itemToSend.appendChild(advice)

            fetch('/music/fcreateME/', {
                method: 'POST',
                credentials: 'same-origin',
                headers: {
                    'Accept': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrftoken,
                },

                body: JSON.stringify({'type': type, 'sp_id': id, 'to': username.value})

            })
                .then(response => response.json())
                .then(data =>{
                    console.log(data)
                    if (data.status === 'failed'){
                        divText.textContent = "Error, you can't send requests to yourself "
                    }
                    else{
                        window.location.href = '/musicexchange/history'

                    }

                })


        }


    })

    Delete.addEventListener('click', () =>{
        console.log('Delete')
        itemToSend.innerHTML = ''
    })


})