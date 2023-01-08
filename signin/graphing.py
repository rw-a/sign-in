import plotly.graph_objects as go
from .models import Person, Signin


def graph_people(people_ids: list):
    people = [Person.objects.get(pk=pk) for pk in people_ids]   # converts the list of ids into a list of Person objects
    signins = Signin.objects.order_by('-date')

    # get every date where there has been a sign in
    dates = []
    for signin in signins:
        date = signin.date.astimezone().date()
        if date not in dates:
            dates.append(date)

    x = [date.strftime("%a %x") for date in dates]  # the x-axis of the heatmap corresponds to the date
    y = [person.name for person in people]          # the y-axis of the heatmap corresponds to the person

    z = []   # the z-axis of the heatmap corresponds to whether the person attended
    for person in people:
        person_z = []
        for date in dates:
            attended = min(person.signin_set.filter(date__date=date).count(), 1)    # 1 if attended, 0 if didn't
            person_z.append(attended)
        z.append(person_z)

    fig = go.Figure(data=go.Heatmap(
        z=z, y=y, x=x,
        hoverinfo='skip',
        colorscale='RdYlGn',
        xgap=1, ygap=1
    ))

    return fig.to_image(format='svg').decode('utf-8')
