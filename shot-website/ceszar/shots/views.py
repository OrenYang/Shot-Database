from django.shortcuts import render
from .models import Shot, Gas
from django.views import generic


def home(request):
    return render(request,
                  "shots/home.html",
                  context={}
                  )

class ShotListView(generic.ListView):
    model = Shot


class ShotDetailView(generic.DetailView):
    model = Shot
