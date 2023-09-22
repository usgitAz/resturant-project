from django.core.exceptions import PermissionDenied
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode 
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings
def DetectUser(user):
    if user.role == 1:
        return "VDashBoard"
    elif user.role == 2:
        return "CDashBoard"
    elif user.role is None and user.is_admin:
        return "/admin"
    
# check permission to visit Customer dashboard or vendor dash board  

def check_role_customer(user):
    if user.role == 2:
        return True
    
    else :
        raise PermissionDenied
    
def check_role_vendor(user):
    if user.role == 1:
        return True
    
    else :
        raise PermissionDenied

#verification with email address 

def send_verification_email (request, user):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    mail_subject = "Verfiy your account with this link !"
    message = render_to_string('accounts/emails/account_verification_email.html',{
        'user' : user ,
        'domain' : current_site,
        'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
        'token' : default_token_generator.make_token(user),
    })
    to_email = user.email
    mail = EmailMessage(mail_subject , message , from_email ,to=[to_email])
    mail.send()


#reset email 

def send_reset_password_email(request , user):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    mail_subject = "Reset Your password with this link ."
    message = render_to_string('accounts/emails/reset_password_email.html',{
        'user' : user ,
        'domain' : current_site,
        'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
        'token' : default_token_generator.make_token(user),
    })
    to_email = user.email
    mail = EmailMessage(mail_subject , message , from_email ,to=[to_email])
    mail.send()