from django.core.management.base import BaseCommand
from site_settings.models import SiteSettings

class Command(BaseCommand):
    help = 'Initialize site settings'

    def handle(self, *args, **kwargs):
        if not SiteSettings.objects.exists():
            SiteSettings.objects.create(
                site_name='Your Site Name',
                meta_title='Your Site',
                meta_description='Your site description',
                meta_keywords='your, keywords',
                footer_text='Your footer text',
                copyright_text='© 2024 Your Company'
            )
            self.stdout.write(self.style.SUCCESS('Site settings initialized'))
