document.addEventListener('DOMContentLoaded', ()=>{

    let username = document.querySelector('#username').textContent
    let pagination_pages = document.querySelector('#pagination_pages')
    let table = document.querySelector('#table')
    let title  = document.querySelector('#title')

      function convertirYFormatearFecha(isoDate) {
        // Convertir la fecha ISO 8601 a un objeto Date
        const date = new Date(isoDate);

        // Convertir la fecha a UTC-6
        const utcMinus6Offset = -6 * 60; // UTC-6 en minutos
        const utcMinus6Date = new Date(date.getTime() + utcMinus6Offset * 60000);

        // Obtener los componentes de la fecha
        const day = utcMinus6Date.getUTCDate();
        const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        const month = monthNames[utcMinus6Date.getUTCMonth()];
        const year = utcMinus6Date.getUTCFullYear();
        const hours = String(utcMinus6Date.getUTCHours()).padStart(2, '0');
        const minutes = String(utcMinus6Date.getUTCMinutes()).padStart(2, '0');

        // Formatear la fecha
          return `${day} ${month} ${year} ${hours}:${minutes} `;
    }


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


function song_renderize(song) {

    let divRow = document.createElement('div');
    divRow.classList.add('row');

    let divImg = document.createElement('div');
    divImg.classList.add('img');
    let aImg = document.createElement('a');
    aImg.href = `/album/${song.fields.song_album_id}`;

    let imgA = document.createElement('img');
    imgA.classList.add('cover-img');
    imgA.setAttribute('src', song.fields.song_cover_url);

    let divLike = document.createElement('div');
    divLike.classList.add('like-icon');

    let btnLike = document.createElement('button');
    btnLike.textContent = 'like';

    let divSongTitle = document.createElement('div');
    divSongTitle.classList.add('song-title');

    let aSongTitle = document.createElement('p');
    aSongTitle.classList.add('text-link-main', 'primary-fs');
    aSongTitle.href = song.fields.song_id;
    aSongTitle.textContent = truncateString(song.fields.song_name);

    let divArtistName = document.createElement('div');
    divArtistName.classList.add('song-title');

    let aArtistName = document.createElement('p');
    aArtistName.classList.add('text-link-main', 'secondary-fs');
    aArtistName.href = `/artist/${song.fields.song_artist_id}`;
    aArtistName.textContent = truncateString(song.fields.song_artist_name);

    let divTimeAgo = document.createElement('div');
    let date = song.fields.timestamp;
    divTimeAgo.textContent = convertirYFormatearFecha(date);

    divSongTitle.appendChild(aSongTitle);
    aImg.appendChild(imgA);
    divImg.appendChild(aImg);
    divLike.appendChild(btnLike);
    divArtistName.appendChild(aArtistName);

    divRow.appendChild(divImg);

    divRow.appendChild(divSongTitle);
    divRow.appendChild(divArtistName);
    divRow.appendChild(divTimeAgo);

    table.appendChild(divRow);
}

function song_renderize2(element, item){
        let divRow = document.createElement('div');
    divRow.classList.add('row');

    let divImg = document.createElement('div');
    divImg.classList.add('img');
    let aImg = document.createElement('p');
    aImg.href = `/album/${element.song_album_id}`;

    let imgA = document.createElement('img');
    imgA.classList.add('cover-img');
    imgA.setAttribute('src', element.song_cover_url);

    if (item === 'Artists')
    {
        imgA.setAttribute('src', element.song_artist_img);
    }

    let divLike = document.createElement('div');
    divLike.classList.add('like-icon');

    let btnLike = document.createElement('button');
    btnLike.textContent = 'like';

    let divSongTitle = document.createElement('div');
    divSongTitle.classList.add('song-title');

    let aSongTitle = document.createElement('p');
    aSongTitle.classList.add('text-link-main', 'primary-fs');
    aSongTitle.href = element.song_id;
    aSongTitle.textContent = truncateString(element.song_album_name);

    if (item === 'Songs')
    {
        aSongTitle.textContent = truncateString(element.song_name);
    }

    let divArtistName = document.createElement('div');
    divArtistName.classList.add('song-title');

    let aArtistName = document.createElement('a');
    aArtistName.classList.add('text-link-main', 'secondary-fs');
    aArtistName.href = `/artist/${element.song_artist_id}`;
    aArtistName.textContent = truncateString(element.song_artist_name);

    let divTimeAgo = document.createElement('div');
    let date = element.count;
    divTimeAgo.textContent = date;

    divSongTitle.appendChild(aSongTitle);
    aImg.appendChild(imgA);
    divImg.appendChild(aImg);
    divLike.appendChild(btnLike);
    divArtistName.appendChild(aArtistName);

    if (item === 'Artists')
    {
        divRow.appendChild(divImg);
        divRow.appendChild(divArtistName);
        divRow.appendChild(divTimeAgo);

        table.appendChild(divRow);
    }
    else{
        divRow.appendChild(divImg);
    divRow.appendChild(divSongTitle);
    divRow.appendChild(divArtistName);
    divRow.appendChild(divTimeAgo);



    table.appendChild(divRow);


    }

}



    // Function to renderize the top albums, artists or songs
    // of an user
    // arguments the top: albums, artists, songs
function topRenderize(item){

          /* this could be a function then i only change the values on body */
    fetch('/music/flibrary/',{
                        method: 'POST',
                        credentials: 'same-origin',
                        headers:{
                            'Accept': 'application/json',
                            'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
                            'X-CSRFToken': csrftoken,
                        },
                                                                        //type can be a variable in dependence of the argument
                        body: JSON.stringify({'username':username, 'type': `${item.toLowerCase()}`, 'date-range': 'all', 'page': 1})

                    })
    .then(response => response.json())
    .then(data =>  {
                    let title  = document.querySelector('#title')
                    //title.textContent = 'All Albums'

                        // erase the table
                        // -> insert the info

                    console.log('the data called ', data)

                    table.innerHTML = ''
                    let startT = document.querySelector('.card2')
                    let prueb = document.createElement('h4')
                    prueb.classList.add('third-fs')

                    prueb.textContent = `Total Rolled: ${data.qty}`
        // FALTA HACER EL DE LA CANTIDAD DE ROLLS AAAAA
        // FALTA HACER EL DE LA CANTIDAD DE ROLLS AAAAA
        // FALTA HACER EL DE LA CANTIDAD DE ROLLS AAAAA

                    title.appendChild(prueb) // HERE IS WHERE I PUT THE NUMBERS
                    data.objects.forEach((element) => {
                        console.log(element.song_album_name)

                        song_renderize2(element, item)

                        })

                        pagination_pages.innerHTML = ''

                        for (let i = 1 ;i <= data.pages; i ++  )
                        {

                            let divItem = document.createElement('div');
                             let pText = document.createElement('p')
                                pText.textContent = i;

                                divItem.classList.add('item');
                                pText.classList.add('textToA');


                            divItem.appendChild(pText)
                            pagination_pages.appendChild(divItem);

                            pText.addEventListener('click', () =>{
                                table.innerHTML = ''
                                 fetch('/music/flibrary/',{
                        method: 'POST',
                        credentials: 'same-origin',
                        headers:{
                            'Accept': 'application/json',
                            'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
                            'X-CSRFToken': csrftoken,
                        },
                                                                        //also here i have albums
                        body: JSON.stringify({'username':username, 'type': `${item.toLowerCase()}`, 'date-range': 'all', 'page': i})

                    })
                    .then(response => response.json())
                    .then(data=> {
                        console.log(data, 'esta data se va a  imprimir')
                        // table.innerHTML = '';
                        data.objects.forEach((song) => {

                            song_renderize2(song, item)})
                    })

                                })

                        }

                    })

}

function rollsR(){

        fetch('/music/flibrary/',{
            method: 'POST',
            credentials: 'same-origin',
            headers:{
                 'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({'username':username, 'type': 'rolls', 'date-range': 'all', 'page': 1})

        })
        .then(response => response.json())
        .then(data=>{
            console.log(data)

            let prueb = document.createElement('h4')
            prueb.classList.add('third-fs')
            prueb.textContent = `${data.qty} Rolls`
            title.appendChild(prueb)

            data.objects.forEach((song) => {
                console.log('line 267', song)
                song_renderize(song)
            })
                pagination_pages.innerHTML = ''

            for (let i = 1; i <= data.pages; i++)
            {

                console.log(i);

                let divItem = document.createElement('div');
                let pText = document.createElement('p')
                pText.textContent = i;

                divItem.classList.add('item');
                pText.classList.add('textToA');

                divItem.appendChild(pText)
                pagination_pages.appendChild(divItem);

                pText.addEventListener('click', () =>{

                    fetch('/music/flibrary/',{
                        method: 'POST',
                        credentials: 'same-origin',
                        headers:{
                            'Accept': 'application/json',
                            'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
                            'X-CSRFToken': csrftoken,
                        },
                        body: JSON.stringify({'username':username, 'type': 'rolls', 'date-range': 'all', 'page': i})

                    })
                    .then(response => response.json())
                    .then(data=> {
                        console.log('linea 301', data)
                        table.innerHTML = '';
                        data.objects.forEach((song) => {
                            console.log('Algoo')

                            song_renderize(song)})
                    })

                })

            }
        })


}


const csrftoken = getCookie('csrftoken');

    rollsR()

    let sections = document.querySelectorAll('.sectionItem');
    sections.forEach((seccion) => {
        seccion.addEventListener('click', () =>{

            title.textContent = `All ${seccion.textContent}`
            console.log(seccion.textContent)
            table.innerHTML = ''

            if (seccion.textContent === 'Rolls')
            {
                console.log('To rollsR')
                rollsR()
            }

            else{
                topRenderize(seccion.textContent)
            }



        })
    })

})