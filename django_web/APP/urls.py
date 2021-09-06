from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'), # start or home page of website 
    path('login_signup_page', views.login_signup_page, name='login_signup_page'), # page for login_signup action
    path('home_page', views.index, name='index'), # page for return from login_signup page to home page
    path('login_check_info', views.login_check_info, name='login_check_info'), # page for checking information of login
    path('signup_check_info', views.signup_check_info, name='signup_check_info'), # page for checking information of signup
    path('log_out', views.log_out, name='log_out'), # method for logging out from accnt 
    path('book_trip_main_btn_action', views.book_trip_main_btn_action, name='book_trip_main_btn_action'),
    path('more_info_main_btn_action', views.more_info_main_btn_action, name='more_info_main_btn_action'),
    path('signup_verification_check_otp_info', views.signup_verification_check_otp_info, name='signup_verification_check_otp_info'),

]


