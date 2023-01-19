from django.urls import path
from . import views
urlpatterns = [
    path('signup/',views.signUp),
    path('product/',views.ProductsView.as_view()),
    path('product/<id>/',views.ProductsView.as_view()),
    path('sell/',views.recordSale),
    path('customers/',views.allCustomers),
    path('sales/user/',views.salesBySeller),
    path('sales/<id>/products/',views.salesProducts),
    path('customers/<cust_id>/',views.updateCustomerDetails),
    path('sale/<sales_id>/',views.productSoldUpdate),
    path('clear/<sales_id>/',views.clearSales),
]
