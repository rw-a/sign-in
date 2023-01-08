import plotly.graph_objects as go
from .models import Person, Signin


def graph_people(people_ids: list):
    people = [Person.objects.get(pk=pk) for pk in people_ids]   # converts the list of ids into a list of Person objects
    signins = Signin.objects.all()

    dates = []
    for signin in signins:
        date = signin.date.astimezone().date()
        if date not in dates:
            dates.append(date)
