from django.urls import path
from users.views import LoginView, SignupView, ProfileView, Update, log_out
from users import views

app_name='users'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='sign'),
    path('<int:pk>/', ProfileView.as_view(), name='profile'),
    path('update/', Update.as_view(), name='update'),
    path('logout/', views.log_out, name='logout'),
    path('verify/<str:key>/', views.confirm_mail, name='chmail'),
]