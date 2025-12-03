from django.core.management import call_command
from django.core.management.base import BaseCommand
from djstripe.enums import PriceType
from djstripe.models import Product
from stripe.error import AuthenticationError

from apps.subscriptions.metadata import ProductMetadata
from apps.utils.billing import create_stripe_api_keys_if_necessary


class Command(BaseCommand):
    help = "Bootstraps your Stripe subscriptions"

    def handle(self, **options):
        print("Syncing products and prices from Stripe")
        try:
            if create_stripe_api_keys_if_necessary():
                print("Added Stripe secret key to the database...")
            # due to an issue in djstripe sometimes failing on unsynced data,
            # we need to sync prices once before syncing both products and prices
            call_command("djstripe_sync_models", "price")
            call_command("djstripe_sync_models", "product", "price")
        except AuthenticationError:
            print(
                "\n======== ERROR ==========\n"
                "Failed to authenticate with Stripe! Check your Stripe key settings.\n"
                "More info: https://docs.saaspegasus.com/subscriptions#getting-started"
            )
        else:
            print("Done! Creating default product configuration")
            _create_default_product_config()


def _create_default_product_config():
    # make the first product the default
    default = True
    product_metas = []
    for product in Product.objects.filter(active=True, default_price__type=PriceType.recurring):
        product_meta = ProductMetadata.from_stripe_product(
            product,
            description=f"The {product.name} plan",
            is_default=default,
            features=_get_features(product),
        )
        default = False
        product_metas.append(product_meta)

    print(
        "Copy/paste the following code into your `apps/subscriptions/metadata.py` file "
        "and then remove any products that you don't want to offer as a subscription:\n\n"
    )
    newline = "\n"
    print(f"ACTIVE_PRODUCTS = [{newline}    {f',{newline}    '.join(str(meta) for meta in product_metas)},{newline}]")


def _get_features(product: Product) -> list[str]:
    features = product.stripe_data.get("marketing_features")
    return (
        [f["name"] for f in features]
        if features
        else [
            f"{product.name} Feature 1",
            f"{product.name} Feature 2",
            f"{product.name} Feature 3",
        ]
    )
