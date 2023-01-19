from django.urls import path
from . import views
urlpatterns = [
    path('catagory/',views.CategoryView.as_view()),
    path('catagory/all/',views.allCategories),
    path('sales/',views.SalesView),
    path('sales/<id>/products/',views.salesProducts)
]
