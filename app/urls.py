from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # path('', views.DataSchemasList.as_view(), name='index'),
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),

    # path('create/<str:pk>/', views.create_schema, name='create_schema'),
    path('create/', views.create_schema, name='create_schema'),

    path('update/<str:pk>/', views.update_schema, name='update_schema'),
    path('delete/<str:pk>/', views.delete_schema, name='delete_schema'),
    path('delete/<str:pk>/<str:col_name>/', views.delete_column, name='delete_column'),


    path('dataset/<str:pk>', views.dataset, name='dataset'),
    path('create_csv/<str:pk>/', views.export_to_csv, name='csv_generator')

]
