import qrcode
import os
from PIL import Image
from django.conf import settings
from datetime import datetime
import random
from .apps import PatientConfig
LOGO_LINK = os.path.join(settings.MEDIA_ROOT, 'logos', 'medwell_qr_logo.png')


def create_qr(token,email):
    logo = Image.open(LOGO_LINK)
    logo = logo.convert("RGBA")
    basewidth = 180
    wpercent = (basewidth / float(logo.size[0]))
    hsize = int((float(logo.size[1]) * float(wpercent)))
    logo = logo.resize((basewidth, hsize))
    QRcode = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )
    QRcode.add_data(token)
    QRcode.make()
    QRcolor = 'Blue'
    QRimg = QRcode.make_image(fill_color=QRcolor, back_color="white").convert('RGBA')
    pos = ((QRimg.size[0] - logo.size[0]) // 2,
        (QRimg.size[1] - logo.size[1]) // 2)
    QRimg.paste(logo, pos, logo)
    path=  os.path.join(settings.MEDIA_ROOT,'qr_codes',email.split("@")[0]+"share_with_Doctor_qr.png")
    QRimg.save(path)
    return path

def create_qr_for_profile(token,email):
    logo = Image.open(LOGO_LINK)
    logo = logo.convert("RGBA")
    basewidth = 180
    wpercent = (basewidth / float(logo.size[0]))
    hsize = int((float(logo.size[1]) * float(wpercent)))
    logo = logo.resize((basewidth, hsize))
    QRcode = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )
    QRcode.add_data(token)
    QRcode.make()
    QRimg = QRcode.make_image( back_color="white").convert('RGBA')
    pos = ((QRimg.size[0] - logo.size[0]) // 2,
        (QRimg.size[1] - logo.size[1]) // 2)
    QRimg.paste(logo, pos, logo)
    path=  os.path.join(settings.MEDIA_ROOT,'qr_codes',email.split("@")[0]+str(random.randint(10000,100000))+".png")
    QRimg.save(path)
    return path


def request_access(doctor_id, patient_id):
    access_key = f"access:{doctor_id}:{patient_id}"
    PatientConfig.redis_client.setex(access_key, 600, "granted")
    print("Request Granted")

def check_access(doctor_id, patient_id):
    access_key = f"access:{doctor_id}:{patient_id}"
    if PatientConfig.redis_client.get(access_key):
        print("Access Exists")
        return True
    else:
        print("Request revoked")
        return False