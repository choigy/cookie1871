from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.conf import settings
# Create your models here.

class User(AbstractUser):
    bio=models.TextField()
    liked=models.CharField(max_length=80, null=True, blank=True)
    salt=models.CharField(max_length=140, null=True, blank=True)
    email_confirmed=models.BooleanField(default=False)
    email_key=models.CharField(max_length=200,null=True, blank=True) 
    
    def verify_email(self):
        if self.email_confirmed==False:
            key=uuid.uuid4().hex[:20]
            self.email_key=key
            html_message=render_to_string(
                'emails/email.html', {'key':self.email_key}
            )
            send_mail(
                'for test send mail',
                strip_tags(html_message),
                'sexy_guy@sandbox088aaeed2a5a4e50afa0f0796808c58d.mailgun.org',
                [self.email],
                fail_silently=False,
            )
            self.save()
        return
            
        
    
    
