from django.urls import path,include
from . import views


urlpatterns = [
    path('login/', views.log_in),
    path('signup/', views.sign_up),
    path('change_password/', views.change_password),
    path('logout/', views.log_out),
    path('function_select/', views.function_select),
    path('message_list/', views.message_list),
    path('account_list/', views.account_list),
    # path('change_password',views.change_password),
]