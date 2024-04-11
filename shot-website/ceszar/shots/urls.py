from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="shots-home"),
    #path("shots/", views.ShotListView.as_view(), name="shots-list"),
    path("shot/<int:pk>", views.ShotDetailView.as_view(), name='shot-detail'),
    path("shot/<int:pk>/summary", views.ShotSummary.as_view(), name='shot-summary'),
    path("shots/", views.shot_list, name="shots-list"),
]
