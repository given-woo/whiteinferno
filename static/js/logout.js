console.log('logout.js running...')

document.getElementsByClassName('logout-button')[0].addEventListener('click', function(event) {
    event.preventDefault();
    fetch('/process_logout/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
    })
    .then((response) => response.json())
    .then((data) => {
        if(data.result == 'Success') {
            window.location.href = '/';
        } else {
            alert('Logout failed');
        }
    });
});
