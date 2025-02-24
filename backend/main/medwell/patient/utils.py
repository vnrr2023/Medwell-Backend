from .apps import PatientConfig
import qrcode
import os
import random
from io import BytesIO
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from PIL import Image
import requests
from django.conf import settings

LOGO_LINK = "https://vnrr-bucket-1.s3.us-east-1.amazonaws.com/logos/medwell_qr_logo.png"


def create_qr(data,email):
    response = requests.get(LOGO_LINK)
    response.raise_for_status()
    logo = Image.open(BytesIO(response.content)).convert("RGBA")
    basewidth = 180
    wpercent = (basewidth / float(logo.size[0]))
    hsize = int((float(logo.size[1]) * float(wpercent)))
    logo = logo.resize((basewidth, hsize))
    QRcode = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )
    QRcode.add_data(data)
    QRcode.make()
    QRcolor = 'Blue'
    QRimg = QRcode.make_image(fill_color=QRcolor, back_color="white").convert('RGBA')
    pos = ((QRimg.size[0] - logo.size[0]) // 2,
        (QRimg.size[1] - logo.size[1]) // 2)
    QRimg.paste(logo, pos, logo)
    img_io = BytesIO()
    QRimg.save(img_io, format='PNG')
    img_io.seek(0)
    filename = f"qr_codes/{email.split('@')[0]}_{random.randint(10000, 100000)}.png"
    file_path = default_storage.save(filename, ContentFile(img_io.getvalue()))
    return default_storage.url(file_path)

def create_qr_for_profile(data,email):
    response = requests.get(LOGO_LINK)
    response.raise_for_status()
    logo = Image.open(BytesIO(response.content)).convert("RGBA")
    basewidth = 180
    wpercent = (basewidth / float(logo.size[0]))
    hsize = int((float(logo.size[1]) * float(wpercent)))
    logo = logo.resize((basewidth, hsize))
    QRcode = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )
    QRcode.add_data(data)
    QRcode.make()
    QRimg = QRcode.make_image( back_color="white").convert('RGBA')
    pos = ((QRimg.size[0] - logo.size[0]) // 2,
        (QRimg.size[1] - logo.size[1]) // 2)
    QRimg.paste(logo, pos, logo)
    img_io = BytesIO()
    QRimg.save(img_io, format='PNG')
    img_io.seek(0)
    filename = f"qr_codes/{email.split('@')[0]}_{random.randint(10000, 100000)}.png"
    file_path = default_storage.save(filename, ContentFile(img_io.getvalue()))
    return default_storage.url(file_path)


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