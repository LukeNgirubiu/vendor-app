from django.urls import path
from . import views
urlpatterns = [
    path('',views.UsersView.as_view(),name="admin.user"),
    path('all/',views.AllUsers,name="user.all"),
]