from django.urls import path
from . import views

urlpatterns = [
    path('admin/form', views.send_email, name="send-email"),
    path('', views.index, name="index")
]
