from cryptography.fernet import Fernet
import jwt
from django.conf import settings
import os
import environ

env=environ.Env()
env_file_path=os.path.join('..', '.env')
environ.Env.read_env(env_file_path)
key=env('CRYPT_KEY')
JWT_SECRET=env("SECRET_KEY")
cipher_suite=Fernet(key)
from urllib.parse import quote



def create_token(payload):
    token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
    encrypted_token = cipher_suite.encrypt(token.encode()).decode()
    return encrypted_token

def decrypt_token(enc_token):
    try:
        dec_token=cipher_suite.decrypt(enc_token.encode()).decode()
        payload = jwt.decode(dec_token, JWT_SECRET, algorithms=['HS256'])
        return {'payload':payload,'status':True}
    except:
        return {'status':False}
    
def create_html_template(payload):
    encrypted_token=quote(create_token(payload))

#     html_upper='''
#     <!DOCTYPE html>
# <html>
# <head>
#     <style>
#         body {
#             font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
#             background-color: #f4f4f4;
#             margin: 0;
#             padding: 0;
#         }
#         .container {
#             background-color: #ffffff;
#             margin: 20px auto;
#             padding: 20px;
#             border-radius: 10px;
#             box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
#             max-width: 600px;
#         }
#         .header {
#             background-color: #4caf50;
#             color: #ffffff;
#             padding: 20px;
#             text-align: center;
#             border-radius: 10px 10px 0 0;
#         }
#         .header h1 {
#             margin: 0;
#             font-size: 24px;
#         }
#         .content {
#             padding: 20px;
#             text-align: center;
#         }
#         .content p {
#             margin: 10px 0;
#             font-size: 16px;
#             color: #333333;
#         }
#         .button {
#             display: inline-block;
#             background-color: #007bff;
#             color: #ffffff;
#             padding: 12px 24px;
#             text-decoration: none;
#             border-radius: 5px;
#             font-size: 16px;
#             margin-top: 20px;
#             transition: background-color 0.3s ease;
#         }
#         .button:hover {
#             background-color: #0056b3;
#         }
#         .footer {
#             margin-top: 30px;
#             font-size: 12px;
#             color: #777777;
#             text-align: center;
#         }
#     </style>
# </head>
# <body>
#     <div class="container">
#         <div class="header">
#             <h1>Welcome to Ettara Cafe</h1>
#         </div>
#         <div class="content">
#             <p>Hello,</p>
#     '''
#     html_lower='''
#             <p>Click the button below to verify your email.</p>
#             <form action="http://127.0.0.1:8000/authentication/verify_mail" method="post">
#                 <input type="hidden" name="token" value="__token__">
#                 <button type="submit" class="button">Verify Email</button>
#             </form>
#         </div>
#         <div class="footer">
#             <p>Thank you for joining Ettara Cafe!</p>
#             <p>If you did not sign up for this account, please ignore this email.</p>
#         </div>
#     </div>
# </body>
# </html>

#     '''
    html_upper=   '''
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email Verification - Medwell</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
        }
        table {
            max-width: 600px;
            margin: 50px auto;
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }
        h1 {
            font-size: 24px;
            color: #333333;
            text-align: center;
        }
        p {
            font-size: 16px;
            line-height: 1.5;
            color: #666666;
            padding: 0 15px;
        }
        a {
            display: inline-block;
            text-decoration: none;
            background-color: #1E90FF;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            font-size: 18px;
            margin: 20px 0;
        }
        .button-container {
            text-align: center;
        }
        .footer {
            padding: 20px;
            background-color: #f4f4f4;
            text-align: center;
            font-size: 12px;
            color: #999999;
        }
    </style>
</head>
<body>
    <table cellpadding="0" cellspacing="0" width="100%">
        <tr>
            <td>
                <table cellpadding="0" cellspacing="0" width="100%">
                    <tr>
                        <td style="background-color: #1E90FF; padding: 30px 0;">
                            <h1 style="color: #ffffff;">Medwell</h1>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 20px;">
                            <h1>Email Verification</h1>
                            <p>Dear User,</p>
                            <p>Thank you for signing up with Medwell. To complete your registration, please verify your email by clicking the button below:</p>
                            <div class="button-container">
        '''
    html_middle='''
                                <a href="http://127.0.0.1:8000/auth/verify_email?token=__token__" target="_blank">Verify Email</a>
                '''
    html_bottom='''
                                </div>
                                <p>If you didn't request this email, please ignore it.</p>
                                <p>Regards,<br>Medwell Team</p>
                            </td>
                        </tr>
                        <tr>
                            <td class="footer">
                                <p>&copy; 2024 Medwell. All rights reserved.</p>
                                <p>This email was sent to you because you registered on Medwell. If you no longer wish to receive these emails, you can unsubscribe at any time.</p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>

    '''
    return html_upper+html_middle.replace('__token__',encrypted_token)+html_bottom
