import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from django.conf import settings

def generate_verification_code():
    """Generate a 6-digit verification code"""
    return str(random.randint(100000, 999999))

def send_qq_email(sender_email, auth_code, recipient_email, subject, body):
    """
    Send email via QQ SMTP server
    
    Args:
        sender_email: Sender's QQ email address
        auth_code: QQ email authorization code (not login password)
        recipient_email: Recipient's email address
        subject: Email subject
        body: Email body content
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    # QQ SMTP settings
    smtp_server = "smtp.qq.com"
    smtp_port = 587  # or 465 for SSL
    
    try:
        # Create message
        message = MIMEMultipart()
        message['From'] = Header(sender_email)
        message['To'] = Header(recipient_email)
        message['Subject'] = Header(subject, 'utf-8')
        
        # Add body to email
        message.attach(MIMEText(body, 'plain', 'utf-8'))
        
        # Create SMTP session
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Enable TLS encryption
        server.login(sender_email, auth_code)  # Use auth code, not password
        
        # Send email
        text = message.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        
        print(f"Email sent successfully to {recipient_email}")
        return True
        
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def send_verification_email(recipient_email, verification_code):
    """
    Send verification code email to user
    
    Args:
        recipient_email: User's email address
        verification_code: 6-digit verification code
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    # Email configuration - these should be in Django settings
    sender_email = getattr(settings, 'EMAIL_SENDER', "3146977024@qq.com")
    auth_code = getattr(settings, 'EMAIL_AUTH_CODE', "xgnlkkhmjknpdeaf")
    
    subject = "Tostada 邮箱验证码"
    body = f"""
您好！

您正在注册 Tostada 账户，您的邮箱验证码是：

{verification_code}

验证码有效期为10分钟，请及时使用。如果这不是您本人的操作，请忽略此邮件。

Tostada 团队
"""
    
    return send_qq_email(sender_email, auth_code, recipient_email, subject, body)