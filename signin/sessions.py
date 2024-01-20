from typing import TypedDict
from django.utils import timezone
from .models import Person, Session


def get_people():
    people = {}
    for person in Person.actives.all():
        people[person.pk] = person.name
    return people


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

        person_signins = person.signin_set.filter(session=session)

        if person_signins.count() == 0:
            # if a person has no sign ins, treat them as signed out
            people[person.pk] = {"name": name, "signed_in": False}
        else:
            last_signin = person_signins.latest("date")  # gets the most recent sign in/out
            people[person.pk] = {"name": name, "signed_in": last_signin.is_signin}
    return people


def get_active_sessions():
    current_time = timezone.now().time()

    return Session.objects.all()\
        .filter(sign_in_time__lte=current_time)\
        .filter(end_time__gt=current_time)


def get_default_session():
    """
    Gets an arbitrary session from the list as a default
    """
    active_sessions = get_active_sessions()

    if len(active_sessions) > 0:
        session = active_sessions.latest("sign_in_time")
    else:
        session = Session.objects.all().latest("sign_in_time")

    return session


def is_sign_in_time(session: Session) -> bool:
    """
    Determines whether the current session should be in the sign-in stage. Returns True if time to
    sign in and returns False if time to sign out.
    """
    current_time = timezone.now().time()
    return current_time < session.sign_out_time