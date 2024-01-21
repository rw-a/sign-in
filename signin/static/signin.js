function signIn(element) {
    const is_signin = element.checked;

    fetch("{% url 'signin:signin_request' %}", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": '{{csrf_token}}'
    },
        credentials: 'same-origin',
        body: JSON.stringify({
            pk: element.value,
            is_signin: is_signin,
            session: "{{ current_session.code }}"
        }),
    })
    .then((response) => response.json())
    .then((data) => {
        console.log('Success:', data);
        updatePeopleCount();
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function updatePeopleCount() {
    const numPeople = document.querySelectorAll('input[type="checkbox"]:checked').length;
    if (numPeople > 0) {
        document.getElementById('peopleCount').innerText = `Signed In: ${numPeople}`;
    } else {
        document.getElementById('peopleCount').innerText = "Nobody is signed in right now";
    }
}
updatePeopleCount();

// Load font size from options
const fontSize = window.localStorage.getItem("fontSize");
document.querySelector('html').style.fontSize = `${fontSize}px`;

// Auto-refresh the page every 5 seconds
setTimeout(() => {
    location.reload();
}, 5000);