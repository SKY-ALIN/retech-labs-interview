from django.urls import path, include
from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path('tasks/', views.TaskViewSet.as_view()),
    path('tasks/<int:pk>/', views.UpdateTaskView.as_view()),
    path('company/', views.CompanyView.as_view()),
    path('user/', views.UserView.as_view()),
    url('auth/', include('rest_framework.urls')),
    # Url for obtaining tokens
    url('auth/get_token/', obtain_auth_token),
]
