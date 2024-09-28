from cryptography.fernet import Fernet
import jwt
import os
import environ
from urllib.parse import quote

env=environ.Env()
env_file_path=os.path.join('..', '.env')
environ.Env.read_env(env_file_path)
key=env('CRYPT_KEY')
JWT_SECRET=env("SECRET_KEY")
cipher_suite=Fernet(key)


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
    
def create_html_template(payload:dict):
    encrypted_token=quote(create_token(payload))
    html_upper=   '''
    <!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email Verification - Medwell</title>
    <style>
        body {
            font-family: 'Helvetica Neue', Arial, sans-serif;
            background-color: #f9fafb;
            margin: 0;
            padding: 0;
        }

        .email-container {
            max-width: 600px;
            margin: 50px auto;
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }

        .email-header {
            background-color: #007bff;
            padding: 20px;
            text-align: center;
        }

        .email-header img {
            width: 150px; /* Adjust the size of the logo as needed */
            margin-bottom: 10px;
        }

        .email-header h1 {
            color: #ffffff;
            font-size: 28px;
            margin: 0;
            font-weight: bold;
        }

        .email-body {
            padding: 30px 20px;
        }

        .email-body h1 {
            font-size: 24px;
            color: #333333;
            text-align: center;
            margin-bottom: 20px;
        }

        .email-body p {
            font-size: 16px;
            line-height: 1.6;
            color: #555555;
            margin: 0;
            margin-bottom: 20px;
            text-align: center;
        }

        .button-container {
            text-align: center;
            margin-bottom: 30px;
        }

        .button-container a {
            display: inline-block;
            text-decoration: none;
            background-color: #007bff;
            color: #ffffff;
            padding: 12px 30px;
            font-size: 18px;
            border-radius: 25px;
            box-shadow: 0 3px 10px rgba(0, 123, 255, 0.3);
            transition: background-color 0.3s ease;
        }

        .button-container a:hover {
            background-color: #0056b3;
        }

        .email-footer {
            background-color: #f9fafb;
            text-align: center;
            padding: 20px;
            color: #999999;
            font-size: 14px;
        }

        .email-footer p {
            margin: 0;
            line-height: 1.5;
        }

        .email-footer a {
            color: #007bff;
            text-decoration: none;
        }

        .email-footer a:hover {
            text-decoration: underline;
        }

        @media screen and (max-width: 600px) {
            .email-container {
                width: 100%;
                border-radius: 0;
            }

            .email-header h1,
            .email-body h1,
            .email-body p {
                font-size: 20px;
            }

            .button-container a {
                padding: 10px 25px;
                font-size: 16px;
            }
        }
    </style>
</head>

<body>
    <div class="email-container">
        <!-- Header Section with Logo -->
        <div class="email-header">
            <img src="https://example.com/logo.png" alt="Medwell Logo"> <!-- Replace with your logo URL -->
            <h1>Medwell</h1>
        </div>

        <!-- Body Section -->
        <div class="email-body">
            <h1>Email Verification</h1>
            <p>Dear User,</p>
            <p>Thank you for registering with Medwell. Please verify your email address to complete the sign-up process by clicking the button below.</p>

            <div class="button-container">
        '''
    html_middle='''
                                <a href="http://127.0.0.1:8000/auth/verify_mail/?token=__token__" target="_blank">Verify Email</a>
                '''
    html_bottom='''
                              </div>

            <p>If you did not create an account with Medwell, please ignore this email.</p>
            <p>Best regards,<br>Medwell Team</p>
        </div>

        <!-- Footer Section -->
        <div class="email-footer">
            <p>&copy; 2024 Medwell. All rights reserved.</p>
            <p>This email was sent to you because you registered on Medwell. If this wasn't you, <a href="#">contact support</a>.</p>
        </div>
    </div>
</body>

</html>
    '''
    return html_upper+html_middle.replace('__token__',encrypted_token)+html_bottom


def create_template_for_otp(payload:dict):
    token=create_token(payload)
    email=payload['email']
    otp_number=payload['otp']
    html_upper='''
    <!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OTP for Password Reset - Medwell</title>
    <style>
        body {
            font-family: 'Helvetica Neue', Arial, sans-serif;
            background-color: #f9fafb;
            margin: 0;
            padding: 0;
        }

        .email-container {
            max-width: 600px;
            margin: 50px auto;
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }

        .email-header {
            background-color: #007bff;
            padding: 20px;
            text-align: center;
        }

        .email-header img {
            width: 150px; /* Adjust logo size */
            margin-bottom: 10px;
        }

        .email-header h1 {
            color: #ffffff;
            font-size: 28px;
            margin: 0;
            font-weight: bold;
        }

        .email-body {
            padding: 30px 20px;
        }

        .email-body h1 {
            font-size: 24px;
            color: #333333;
            text-align: center;
            margin-bottom: 20px;
        }

        .email-body p {
            font-size: 16px;
            line-height: 1.6;
            color: #555555;
            margin: 0;
            margin-bottom: 20px;
            text-align: center;
        }

        .otp-box {
            display: inline-block;
            background-color: #f0f0f0;
            border-radius: 8px;
            padding: 15px 30px;
            font-size: 24px;
            font-weight: bold;
            color: #333333;
            text-align: center;
            margin-bottom: 30px;
        }

        .otp-container {
            text-align: center;
            margin: 30px 0;
        }

        .email-footer {
            background-color: #f9fafb;
            text-align: center;
            padding: 20px;
            color: #999999;
            font-size: 14px;
        }

        .email-footer p {
            margin: 0;
            line-height: 1.5;
        }

        .email-footer a {
            color: #007bff;
            text-decoration: none;
        }

        .email-footer a:hover {
            text-decoration: underline;
        }

        @media screen and (max-width: 600px) {
            .email-container {
                width: 100%;
                border-radius: 0;
            }

            .email-header h1,
            .email-body h1,
            .email-body p {
                font-size: 20px;
            }

            .otp-box {
                font-size: 22px;
                padding: 10px 25px;
            }
        }
    </style>
</head>

<body>
    <div class="email-container">
        <!-- Header Section with Logo -->
        <div class="email-header">
            <img src="https://example.com/logo.png" alt="Medwell Logo"> <!-- Replace with your logo URL -->
            <h1>Medwell</h1>
        </div>

        <!-- Body Section -->
        <div class="email-body">
            <h1>OTP for Password Reset</h1>
    '''
   
    html_middle= f'''
            <p>Dear {email} </p>
            <p>We received a request to reset your password. Use the following OTP to complete the process:</p>

            <!-- OTP Display -->
            <div class="otp-container">
                <div class="otp-box">
    '''
    html_bottom='''
     </div>
            </div>

            <p>Please enter this OTP within 10 minutes. If you didn't request a password reset, you can safely ignore this email.</p>
            <p>Best regards,<br>Medwell Team</p>
        </div>

        <!-- Footer Section -->
        <div class="email-footer">
            <p>&copy; 2024 Medwell. All rights reserved.</p>
            <p>If this wasn't you, <a href="#">contact support</a>.</p>
            </div>
        </div>
    </body>

    </html>
    '''
    return {'token':token,'html':html_upper+html_middle+str(otp_number)+html_bottom}