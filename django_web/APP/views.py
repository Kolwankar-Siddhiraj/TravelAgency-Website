from typing import final
from django.http import request
from django.shortcuts import render
from .models import *
import re
import smtplib 
import random
from django.contrib.auth.models import User, auth 
from time import * 


# Create your views here.
 
# custome members 
# Initilization OR declaring varibles 
background_img_of_body = ["pic01.jpg", "pic02.jpg", "pic03.jpg", "pic04.jpg", "pic05.jpg", "pic06.jpg", "pic07.jpg"]
user1 = str("username_db")
password_db = str("password_db")
email_pattern = "[a-zA-Z0-9]+@[a-zA-Z]+\.(com|net|in)"
username_pattern = "[a-zA-Z]"
otp_verification_pattern = "[0-9]"
otp_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
host_email_addr = 'sample@gmail.com'
host_email_pass = 'password'
otp = ""


class Data:
    id : int 
    imgbd : str
    imgdiv : str
    userid : str
    log_btn_action : str
    login_status : bool
    # for login information check
    check_email : bool
    check_pass : bool
    # for signup information check
    s_email : bool
    s_userid : bool
    s_pass : bool
    s_repass : bool
    # for E-mail verification OR OTP checking
    check_otp : bool
    user_email_show_to_verify : str

obj = Data()
obj.imgbd = random.choice(background_img_of_body) # changing body background
obj.imgdiv = 'konkan.jpg'
obj.userid = "Login"
obj.check_email = False
obj.check_pass = False
obj.log_btn_action = "login_signup_page"
obj.login_status = False
obj.s_email = False
obj.s_userid = False
obj.s_pass = False
obj.s_repass = False


# Getting object of all destination data from database
dests = Destination.objects.all()


def index(request): # homepage of website
    # Getting object of all destination data from database
    dests = Destination.objects.all()
    obj.imgbd = random.choice(background_img_of_body) # changing body background
    return render(request, 'index.html', {'obj':obj, 'destination_list':dests})

def login_signup_page(request): # page for login and signup >> main login button press action 
    obj.check_email = False
    obj.check_pass = False
    obj.s_email = False
    obj.s_userid = False
    obj.s_pass = False
    obj.s_repass = False

    obj.imgbd = random.choice(background_img_of_body) # changing body background
    return render(request, 'login_signup_page.html', {'obj':obj})

# page for checking information of login from > login_signup page >> login button press action
def login_check_info(request):
    userid_login = str(request.POST["userid_login"])
    password_login = str(request.POST["password_login"])
    obj.check_email = False
    obj.check_pass = False
    verification_result = check_info_for_login(userid_login, password_login, request)

    print("Login information...#")
    print("Email :: ", userid_login)
    print("Password :: ", password_login)

    # Based on final result of Var.. verification_result return a page
    # if verification result is true return Main Home Page .. else return same page to login again
    if verification_result:
        # Getting object of all destination data from database
        dests = Destination.objects.all()
        obj.imgbd = random.choice(background_img_of_body) # changing body background
        return render(request, 'index.html', {'obj':obj, 'destination_list':dests})
    else:
        obj.imgbd = random.choice(background_img_of_body) # changing body background
        return render(request, 'login_signup_page.html', {'obj': obj})

# Method > login_check_info < ends here 

def check_info_for_login(userid, password, req):
    # initilize parameters 
    userid_login = userid
    password_login = password
    request = req
    # initilizing a verification_result variable to false
    verification_result = False
    #check E-mail
    if re.search(email_pattern, userid_login):
        if User.objects.filter(email=userid_login):
            print("valid e-mail")
            print("Regesistered user.!")
        else:
            obj.check_email = True
            obj.check_pass = True
            verification_result = False
            print("Not regesistered user.!")
    else:
        obj.check_email = True
        obj.check_pass = True
        verification_result = False
        print("Invalid e-mail")

    # checking login information 
    user = auth.authenticate(username=userid_login, password=password_login)

    if user is not None:
        auth.login(request, user) # giving login permission to user
        obj.log_btn_action = "#"
        obj.login_status = True
        name_of_user = User.objects.get(username=userid_login)
        obj.userid = name_of_user.first_name
        verification_result = True
        print("Verification success.!")
    else:
        obj.check_email = True
        obj.check_pass = True
        verification_result = False
        print("Verification failed.!")

    # returning true OR false on basis of the information provided by user
    return verification_result

# Method > check_info_for_login < ends here

# initilizing for global scope
email_signup = ''
username_signup = ''
password_signup = ''

# page for cheking information of signup from > login_signup page >> signup button press action
def signup_check_info(request): 

    global email_signup 
    global username_signup
    global password_signup

    email_signup = str(request.POST["email_signup"])
    username_signup = str(request.POST["userid_signup"])
    password_signup = str(request.POST["password_signup"])
    re_password_signup = str(request.POST["re_password_signup"])

    final_res = False
    obj.s_email = False
    obj.s_userid = False
    obj.s_pass = False
    obj.s_repass = False
    obj.userid = username_signup

    print("Signup information...#")
    print("Email :: ", email_signup)
    print("username :: ", username_signup)
    print("Password :: ", password_signup)
    print("Re password :: ", re_password_signup)
    #check E-mail
    if re.search(email_pattern, email_signup):
        print("valid e-mail")
    else:
        obj.s_email = True
        final_res = True
        print("Invalid e-mail")
    #checking username
    if re.search(username_pattern, username_signup):
        print("Valid username")
    else:
        obj.s_userid = True
        final_res = True
        print("Invalid username")
    #cheking password
    if password_signup == re_password_signup:
        print("Valid password")
    else:
        obj.s_pass = True
        obj.s_repass = True
        final_res = True
        print("Invalid password")

    #cheking final result
    if final_res == True: # True means some or all information filled by user is incorrect.. so return same page and try to collect correct infornation 
        obj.imgbd = random.choice(background_img_of_body) # changing body background
        return render(request, 'login_signup_page.html', {'obj': obj})
    elif final_res == False: # False means all information filled by user is correct .. so return page for e-mail verification 
        obj.user_email_show_to_verify = email_signup # user e-mail addrs 
        obj.check_otp = False
        # sending otp on email provided by user while signing up
        print("otp sending..!")
        # calling method to send otp to user on his email
        send_email_otp()
        print("otp sent successfully..!")
        obj.imgbd = random.choice(background_img_of_body) # changing body background
        # render next page of verification of otp
        return render(request, 'signup_verification.html', {'obj':obj})
    else:
        print("Something went wrong...!!!")

# Method > signup_check_info < ends here

# method for sending email of otp to users
def send_email_otp():
    global otp
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(host_email_addr, host_email_pass)
        # calling method for generating otp  
        otp = generate_otp()
        subject = 'From Travel India :: OTP for verifying your E-mail.'
        body = '\n\n\nThe otp for login is '+otp+'. Don`t share with anyone.'
        msg = f'Subject: {subject}\n\n\n{body}'

        smtp.sendmail(host_email_addr, email_signup, msg)
        print("E-mail sent successfully..!")

# Method > send_email_otp < ends here

# method for generating a otp to serify email
def generate_otp():
    otp = ""
    for i in range(6):
        otp = str(otp + random.choice(otp_list))
        print("otp : ", otp)
    print("final otp is : ", otp)
    print("otp generated successfully..!")
    return otp
# Method > generate_otp < ends here

# checking otp information and verifying
def signup_verification_check_otp_info(request):
    
    #checking for user already logged in or not
    if obj.login_status == False:
        pass
    else:
        otp_signup_verification = str(request.POST['otp_signup_verification'])
        print("OTP :: ", otp_signup_verification) 
        global otp
        # verification of otp 
        if len(otp_signup_verification) == 6:
            if re.search(otp_verification_pattern, otp_signup_verification):
                if otp_signup_verification == otp:
                    print("OTP verification success..!") 
                    print("Name User :: ", obj.userid)
                    obj.log_btn_action = "#"
                    obj.login_status = True
                    # saving user data in database
                    new_user = User.objects.create_user(username=email_signup, password=password_signup, email=email_signup, first_name=username_signup)
                    new_user.save()
                    print("New user information saved in database")

                    # Getting object of all destination data from database
                    dests = Destination.objects.all()
                    obj.imgbd = random.choice(background_img_of_body) # changing body background
                    return render(request, 'index.html', {'obj':obj, 'destination_list':dests})
                else:
                    print("OTP verification failed..!, No matched")
                    obj.imgbd = random.choice(background_img_of_body) # changing body background
                    return render(request, 'signup_verification.html', {'obj':obj})
                    # end of if
            else:
                print("OTP verification failed..!, Not received")
                obj.imgbd = random.choice(background_img_of_body) # changing body background
                return render(request, 'signup_verification.html', {'obj':obj})
                # end of if
        else:
            obj.check_otp = True
            obj.imgbd = random.choice(background_img_of_body) # changing body background
            return render(request, 'signup_verification.html', {'obj':obj})

# Method > signup_verification_check_otp_info < ends here

# method for booking a trip of my destination from my site
def book_trip_main_btn_action(request): 
    return render(request, 'book_trip_main_btn_action.html', {'obj':obj})
# Method > book_trip_main_btn_action < ends here

# method for knowing more information about my respective trip 
def more_info_main_btn_action(request): 
    return render(request, 'more_info_main_btn_action.html')
# Method > more_info_main_btn_action < ends here

# method for logging out from site 
def log_out(request): 
    obj.userid = "login"
    obj.log_btn_action = "login_signup_page"
    obj.login_status = False
    
    # Getting object of all destination data from database
    dests = Destination.objects.all()
    obj.imgbd = random.choice(background_img_of_body) # changing body background
    return render(request, 'index.html', {'obj':obj, 'destination_list':dests})

# Method > log_out < ends here
