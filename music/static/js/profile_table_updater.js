document.addEventListener('DOMContentLoaded', ()=>{
    function truncateString(str) {
    if (str.length > 40) {
        return str.substring(0, 37) + '...';
    }
    return str;
}
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

    let username = document.querySelector('#username').textContent
    setInterval(() =>{

        fetch('/music/ats/',{
            method: 'POST',
            credentials: 'same-origin',
            headers:{
                 'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({'username':username, 'test': 777})

        })
        .then(response => response.json())
        .then(data=>{
            console.log(data)

            if(data.status === 'playing')
            {

                let songsTable = document.querySelector('#table')
                console.log(songsTable)
                console.log(777,data.playing, data.history[0])
                console.log(888,data.playing, data.history[0])
                //-------------------------------------------------------------------------------
                console.log(333, data.playing.item.id,  data.history[0].fields.song_id)
                // gotta put an if to validate if the actual song is the same as the last history

                // main element
                let divRow = document.createElement('div')
                divRow.classList.add('row')
                let divImg = document.createElement('div')
                divImg.classList.add('img')
                let aImg = document.createElement('a')
                // --- Url to the album page ---------------------------------------
                aImg.href = `/album/${data.playing.album.id}`

                let imgA = document.createElement('img')
                imgA.setAttribute('src', data.playing.item.album.images[0].url)

                // ---------- div to the button (or) whatever i'll use ------------------- //
                let divLike = document.createElement('div')
                divLike.classList.add('like-icon')

                let btnLike  = document.createElement('button').textContent = 'like'
                // ----------------------------------------------------------------------- //

                let divSongTitle = document.createElement('div')
                divSongTitle.classList.add('song-title')

                let aSongTitle = document.createElement('a')
                aSongTitle.href = data.playing.item.id
                aSongTitle.textContent = truncateString(data.playing.item.name)

                let divArtistName  = document.createElement('div')
                divArtistName.classList.add('song-title')

                let aArtistName  = document.createElement('a')
                aArtistName.textContent =  truncateString(data.playing.artists[0].name)

                let divTimeAgo = document.createElement('div')
                divTimeAgo.textContent = 'Rollong rn'


                // Make the element









            }

        })



    }, 20000)

})