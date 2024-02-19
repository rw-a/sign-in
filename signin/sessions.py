from datetime import datetime
from zoneinfo import ZoneInfo
from typing import TypedDict, Literal
from django.conf import settings
from django.utils import timezone
from .models import Person, Session


def person_is_signed_in(person: Person, session: Session) -> Literal[0, 1]:
    person_signins = person.signin_set.filter(session=session)

    if person_signins.count() == 0:
        # If a person has no sign ins, treat them as signed out
        return 0
    else:
        # Gets the most recent sign in/out to check
        last_signin = person_signins.latest("date")

        # Use int instead of bool because bool cannot be converted to JavaScript
        return 1 if last_signin.is_signin else 0


def get_people_by_session():
    sessions: dict[str, dict[str, str]] = {}

    for session in Session.objects.all():
        people: dict[str, str] = {}

        for person in session.person_set.filter(hidden=False):
            people[person.pk] = person.name

        sessions[session.code] = people

    return sessions


def get_people_for_spinner():
    class PersonDetails(TypedDict):
        is_signed_in: Literal[0, 1]     # Instead of bool
        days_added_ago: int             # How many days ago the person was added

    # Maps a session cde to a list of people
    sessions: dict[str, dict[str, PersonDetails]] = {}

    for session in Session.objects.all():
        # Maps a person's name to their details
        people: dict[str, PersonDetails] = {}

        for person in session.person_set.filter(hidden=False):
            person_details: PersonDetails = {
                "is_signed_in": person_is_signed_in(person, session),
                "days_added_ago": (timezone.now() - person.date_added).days
            }
            people[person.name] = person_details

        sessions[session.code] = people

    return sessions


def get_people_signin_status(session: Session):
    class PersonType(TypedDict):
        name: str
        signed_in: bool

    # signed_in determines if it gets signed in people (True) or signed out people (False)
    people: dict[str, PersonType] = {}     # dict with pk as key and name as value

    for person in session.person_set.filter(hidden=False):
        name = person.name
        if not person.media_permission:
            name += "﹒"

        people[person.pk] = {"name": name, "signed_in": person_is_signed_in(person, session)}

    return people


def get_active_sessions():
    current_time = datetime.now(ZoneInfo(settings.TIME_ZONE)).time()

    return Session.objects.all()\
        .filter(sign_in_time__lte=current_time)\
        .filter(end_time__gt=current_time)


def get_default_session():
    """
    Choose the most appropriate session if none is specified
    """
    active_sessions = get_active_sessions()

    if len(active_sessions) > 0:
        # Choose one which is active, if possible
        session = active_sessions.earliest("sign_in_time")
    else:
        # Otherwise, choose one arbitrarily
        session = Session.objects.all().earliest("sign_in_time")

    return session


def is_sign_in_time(session: Session) -> bool:
    """
    Determines whether the current session should be in the sign-in stage. Returns True if time to
    sign in and returns False if time to sign out.
    """
    current_time = timezone.now().time()
    return current_time < session.sign_out_time
