const csrftoken = getCookie('csrftoken');

function editPost(event, postId) {
    event.preventDefault()

    const form = document.getElementById(`edit-post-${postId}`)
    const content = document.getElementById(`post-content-${postId}`)

    // display the form to edit the post
    form.classList.remove('d-none')
    content.classList.add('d-none')
}

function closePostEdit(event, postId) {
    event.preventDefault()

    const form = document.getElementById(`edit-post-${postId}`)
    const content = document.getElementById(`post-content-${postId}`)

    form.classList.add('d-none')
    content.classList.remove('d-none')
}

function canclePostEdit(event, postId) {
    closePostEdit(event, postId)
}

function saveEditedPost(event, postId) {
    event.preventDefault()

    const postElemnt = document.getElementById(`post-content-${postId}`)
    const content = new FormData(event.target).get('content')
    const url = event.target.getAttribute('action')

    const request = new Request(
        url,
        {
            method: 'POST',
            mode: 'same-origin',
            headers: { 'X-CSRFToken': csrftoken },
            body: JSON.stringify({content})
        }
    )

    fetch(request)
    .then(response => response.json())
    .then(result => {
        postElemnt.innerHTML = result.content
        console.log('Success:', result)
    })
    .catch(error => console.log('Error:', error))

    closePostEdit(event, postId)
}

function toggleLike(event, id) {
    event.preventDefault()

    const url = event.currentTarget.getAttribute('href')
    const likescountElement = document.getElementById(`likes-count-${id}`)

    const request = new Request(
        url,
        {
            method: 'POST',
            mode: 'same-origin',
            headers: { 'X-CSRFToken': csrftoken }
        }
    )

    fetch(request)
    .then(response => response.json())
    .then(result => {
        likescountElement.innerText = result.likesCount

        console.log('Success:', result)
    })
    .catch(error => console.log('Error:', error))
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