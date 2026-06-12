from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_user, name='login'),
    path('dashboard/', views.index, name='index'),

    path('add/', views.add_product, name='add_product'),
    path('edit/<int:id>/', views.edit_product, name='edit_product'),
    path('delete/<int:id>/', views.delete_product, name='delete_product'),

    path('stock/', views.stock_transaction, name='stock_transaction'),
    path('transactions/', views.transactions, name='transactions'),
    path('category-report/', views.category_report, name='category_report'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
]