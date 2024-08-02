import json
from django.core.management.base import BaseCommand
from usermanagement.models import Country

class Command(BaseCommand):
    help = "Create countries list"
    
    def handle(self, *args, **options):
        json_path = "D:/socialapp/social_app/countries.json"
        
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for item in data:
                Country.objects.update_or_create(
                    name = item.get('name'),
                    defaults={
                        'phone_code':item.get('phone_code'),
                        'longitude':item.get('longitude'),
                        'latitude':item.get('latitude'),
                        'zone_name':item['timezones'][0]['zoneName'] if item.get('timezones') else None,
                        'gmtoffsetname':item['timezones'][0]['gmtOffsetName'] if item.get('timezones') else None,
                    }
                )
            self.stdout.write(self.style.SUCCESS('Successfully imported countries'))