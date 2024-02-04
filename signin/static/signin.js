function signIn(event) {
    const element = event.target;
    const is_signin = element.checked;
    const pk = element.value;

    people[pk]["signed_in"] = is_signin;

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
        console.log('Success:', data);
        updatePeopleCount();
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function renderPeople() {
    const peopleList = document.getElementById("peopleList");

    for ([pk, person] of Object.entries(people)) {
        const container = document.createElement("div");
        container.className = "form-check ps-0";

        const label= document.createElement("label");
        label.className = "person-card form-check-label w-100 py-1 ps-2 mb-2 border border-1 rounded";
        label.htmlFor = pk;
        label.innerText = person.name;

        const input = document.createElement("input");
        input.className = "form-check-input d-none";
        input.type = "checkbox";
        input.id = pk;
        input.value = pk;
        input.title = person.name;
        input.onclick = signIn;
        if (person.signed_in) {
            input.checked = true;
        }

        container.appendChild(label);
        container.appendChild(input);
        peopleList.appendChild(container);
    }
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

updatePeopleCount();
renderPeople();