# Sign In System

## Overview
A website to manage signing in/out of events.

1. Create at session with a specified start/end time.
2. Add users and specify what sessions they would like to attend.
3. Open the session sign-in page on a device (e.g. iPad) accessible to users.
4. Users sign-in using the device.

## Features
- Simple front end for users to sign in/out.
- Store important information about each attendee (e.g. emergency contact details).
- Supports multiple concurrent sessions.
- Analytics to provide insight into attendance trends.
- Spinner to randomly choose a person from a session.


## Depreciated Features
- QR code scanner for quick sign in/out.
- Built-in QR code generator.

## Technical Overview
- Django backend using sqlite3 database.
- Frontend uses Django HTML templates, vanilla JavaScript, and Bootstrap for styling.