import json
import os
import random
import string
import threading

from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def id_generator(size=5, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for x in range(size))


# def CheckTrueFalseLowerCase(itemToCheck):
#     if itemToCheck == 'true':
#         itemToCheck = True
#     else:
#         itemToCheck = False
#     return itemToCheck

class SaveForImg():
    def saveImg(element, instance, table, slug, url, tab):
        for img in element:
            instance.otherImg = img
            instance.save()
            new = table.objects.get(slug=slug)
            if len(tab) != 0:
                qw = url + str(str(str(new.otherImg)).split()
                               ).replace("['", '').replace("']", '')
                tab.extend(qw.split())
            else:
                tab.append(url + str(new.otherImg))
        instance.saveOtherImg = json.dumps(tab)
        return instance.save()


# ********************************************** about email ***************************************************
class EmailThread(threading.Thread):
    ###################### send email faster #####################
    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()


def sendMessage(subject, path, messages, sender, recipient):
    email_subject = subject
    message = render_to_string(path, messages)
    text_content = strip_tags(message)
    email_message = EmailMultiAlternatives(
        email_subject,
        text_content,
        sender,
        recipient,  # email a qui on envoie le message
    )
    email_message.attach_alternative(message, "text/html")
    # email_message.send(fail_silently=False)
    EmailThread(email_message).start()


def deletePathImage(tab):
    # je remplace media par le vide car dans settings.MEDIA_ROOT nous avons deja /media
    # efface les images
    for fil in tab:
        if os.path.exists(settings.MEDIA_ROOT + fil.replace('/media', '')):
            os.remove(settings.MEDIA_ROOT + fil.replace('/media', ''))
        else:
            pass
