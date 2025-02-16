from django.urls import path
from . import views

app_name = 'consultations'

urlpatterns = [
    path('book/', views.book_consultation, name='book_consultation'),
    path('my-consultations/', views.my_consultations, name='my_consultations'),
]
