from django.shortcuts import render
import datetime


# Create your views here.


def home_view(request):
    day = datetime.date.today()
    context = {
        'day': day,
    }
    return render(request, 'home/home_page.html', context)
