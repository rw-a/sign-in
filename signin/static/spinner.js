import {Wheel} from 'https://cdn.jsdelivr.net/npm/spin-wheel@4.3.1/dist/spin-wheel-esm.js';

// Initialise buttons to select session
for (const element of document.querySelectorAll('button[class~="session"]')) {
    element.addEventListener('click', () => {
        selectSession(element.id);
    })
}

// Initialise spinner using selected session
function selectSession(session_code) {
    const signedInOnly = document.getElementById("signed_in_only").checked;

    const items = signedInOnly
        ? Object.entries(people[session_code])
            .filter(([name, signedIn]) => signedIn)
            .map(([name, signedIn]) => {return {label: name}})
        : Object.keys(people[session_code])
            .map((p) => {return {label: p}});

    const resistance = Number(localStorage.getItem("spinnerResistance") || "100");

    const props = {
        items: items,
        itemLabelFontSizeMax: 100,
        radius: 0.84,
        itemLabelRadius: 0.95,
        itemLabelRadiusMax: 0.35,
        itemLabelFont: 'Amatic SC',
        itemLabelBaselineOffset: -0.07,
        itemLabelRotation: 180,
        itemLabelAlign: 'left',
        itemLabelColors: ['#fff'],
        itemBackgroundColors: ['#ffc93c', '#66bfbf', '#a2d5f2', '#515070', '#43658b', '#ed6663', '#d54062' ],
        overlayImage: spinnerOverlayImage,
        image: spinnerImage,
        isInteractive: false,
        rotation: Math.random() * 360,
        rotationSpeedMax: 1000,
        rotationResistance: -resistance
    }

    // Initialise spinner
    const container = document.getElementById('wheel-wrapper');
    const wheel = new Wheel(container, props);

    // Hide options
    document.getElementById('spinner_options').hidden = true;

    // Initialise spin button
    const spinButton = document.getElementById('spin_button');
    spinButton.hidden = false;
    spinButton.addEventListener('click', () => {
        const spinSpeed = Number(localStorage.getItem("spinnerSpeed") || "500");
        wheel.spin(spinSpeed * (Math.random() + 1));
    })
}