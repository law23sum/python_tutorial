from django.conf import settings
from django.core.mail import send_mail
from pydantic_ai.toolsets import FunctionToolset


async def send_email(email: str, subject: str, body: str) -> bool:
    """Send an email to a recipient.

    Args:
        email: The email address of the recipient.
        subject: The subject of the email.
        body: The body of the email.
    """
    send_mail(
        subject=subject,
        message=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )


email_toolset = FunctionToolset(tools=[send_email])
