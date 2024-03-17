// List of PKs of people that have been recently signed in/out by this client
const recentlySignedInPeople = [];

function signIn(element) {
    const is_signin = element.checked;
    const pk = element.value;

    recentlySignedInPeople.push(pk);

    fetch(api_signin_path, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": csrf_token
        },
        credentials: 'same-origin',
        body: JSON.stringify({
            pk: pk,
            is_signin: is_signin,
            session: current_session_code
        }),
    })
    .then((response) => response.json())
    .then((data) => {
        // console.log('Success:', data);
        updatePeopleCount();
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function updatePeople() {
    fetch(`${api_signin_path}?session=${current_session_code}`)
    .then((response) => response.json())
    .then((data) => {
        for ([pk, person] of Object.entries(data)) {
            // Don't override recent changes made by this client
            if (recentlySignedInPeople.includes(pk)) {
                continue;
            }

            const personCheckbox = document.getElementById(pk);

            if (Boolean(person.signed_in) !== Boolean(personCheckbox.checked)) {
                personCheckbox.checked = person.signed_in;
            }
        }

        updatePeopleCount();

        recentlySignedInPeople.length = 0;  // Clear array
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

// Load font size from options
const fontSize = window.localStorage.getItem("fontSize") || "16";
document.querySelector('html').style.fontSize = `${fontSize}px`;

updatePeople();
setInterval(updatePeople, 5000);