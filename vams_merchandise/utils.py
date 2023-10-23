from hashids import Hashids
from django.conf import settings
from django.core.mail import send_mail
from celery import shared_task
from .celery import app

hashids = Hashids(settings.HASHIDS_SALT, min_length=8)

welcome_user_email = """Dear Customer,

We are thrilled to welcome you to VamsCentral, your one-stop destination for an unparalleled online shopping experience! 🛍️

At VamsCentral, we are committed to making your shopping journey enjoyable, convenient, and rewarding. As a valued member of our growing family, you'll discover a world of benefits:

✨ Wide Selection: Explore a vast collection of products ranging from fashion, electronics, home essentials, and much more. With thousands of options at your fingertips, you're sure to find exactly what you need.

🚚 Speedy Delivery: Our dedicated team ensures swift and secure deliveries right to your doorstep, so you can enjoy your purchases without delay.

🛡️ Secure Shopping: Your security is our top priority. Rest assured that your personal information is protected with state-of-the-art security measures.

💎 Exclusive Offers: Be the first to know about our latest promotions, discounts, and exclusive deals. Don't miss out on incredible savings!

🤝 Dedicated Support: Our friendly and knowledgeable support team is here to assist you with any questions or concerns. We're just a message away.

🌟 Personalized Experience: Tailored recommendations and personalized offers await you, ensuring that your shopping experience is uniquely yours.

To kickstart your journey with us, we're delighted to offer you a special [Discount/Welcome Gift]. Simply use the code [CODE] at checkout to redeem your welcome gift.

Ready to start shopping? Visit www.vamscentral.com today and explore the world of endless possibilities.

Thank you for choosing VamsCentral. We can't wait to accompany you on your shopping adventures!

Happy Shopping!

Warm regards,

Anand S.
Founder, VAMSCentral
"""

user_added = """



"""


def h_encode(id):
    
    return hashids.encode(id)


def h_decode(h):
    z = hashids.decode(h)
    if z:
        return z[0]


class HashIdConverter:
    regex = '[a-zA-Z0-9]{8,}'

    def to_python(self, value):
        return h_decode(value)

    def to_url(self, value):
        return h_encode(value)
    
class FloatConverter:
    regex = '[\d\.\d]+'
    # regex = '[0-9]'

    def to_python(self, value):
        return float(value)

    def to_url(self, value):
        return '{}'.format(value)

class RomanNumeralConverter:
    regex = '[MDCLXVImdclxvi]+'

    def to_python(self, value):
        return str(value)

    def to_url(self, value):
        return '{}'.format(value)

@app.task
def send_welcome_email(subject, message, recipient_email,user=None):
    # Send email to admin
    admin_email = settings.ADMIN_EMAIL
    if user:
        admin_message = f"""
        Dear Admin,

        I hope this message finds you well. I wanted to inform you that we have a new member who has recently joined our circle.

        User Information:
        - Name: {user.first_name +' '+user.last_name}
        - Email: {user.email}
        - Username: {user.username}
        - Role: Customer
        - Contact Number: {user.mobileno}

        Please join us in extending a warm welcome to {user.username}. They bring valuable skills and perspectives to our circle, and we believe their presence will greatly contribute to our goals and objectives.

        As the admin, your guidance and support are highly appreciated in helping {user.username} integrate smoothly into our community. If you have any specific onboarding procedures or tasks that you would like to assign to them, please feel free to communicate that to them or delegate accordingly.

        If you have any questions or need further information about the new member, please don't hesitate to reach out to me or directly contact {user.username} at {user.email} or {user.mobileno}.

        Thank you for your continued dedication to our circle, and let's look forward to a fruitful collaboration with our new member.

        Best regards,

        Anand S.
        Director
        VAMSCentral"""
        
    try:
        send_mail(
            subject,
            admin_message,
            settings.DEFAULT_FROM_EMAIL,
            [admin_email],
            fail_silently=False,
        )

        # Send email to user
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient_email],
            fail_silently=False,
        )
        return True
    except:
        return False