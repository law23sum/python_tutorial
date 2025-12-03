from django.core.management.base import BaseCommand
from djstripe.models import Account, WebhookEndpoint

from apps.web.meta import absolute_url


class Command(BaseCommand):
    help = "Sets up Stripe webhooks for local development"

    def add_arguments(self, parser):
        parser.add_argument(
            "--secret",
            help="Optional webhook secret to set on the endpoint",
            required=False,
        )

    def handle(self, **options):
        print("Setting up development webhooks...")
        stripe_account = Account.objects.get()
        webhook_id = "djstripe-development-webhook"
        webhook_data = {
            "url": absolute_url(""),
            "djstripe_owner_account": stripe_account,
            "enabled_events": ["*"],
        }
        if options.get("secret"):
            webhook_data["secret"] = options["secret"]

        endpoint, created = WebhookEndpoint.objects.update_or_create(
            id=webhook_id,
            defaults=webhook_data,
        )
        endpoint_url = f"/stripe/webhook/{endpoint.djstripe_uuid}/"
        print(f"Your webhook endpoint is: {absolute_url(endpoint_url)}")
        print(f"""Run the Stripe cli with:
stripe listen --forward-to {absolute_url(endpoint_url)} {'-H "x-djstripe-webhook-secret: $(stripe listen --print-secret)"' if not options.get("secret") else ""}
""")  # noqa: E501
