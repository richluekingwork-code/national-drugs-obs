from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import County, District

@receiver(post_migrate)
def create_default_counties_and_districts(sender, **kwargs):

    data = {
        "Montserrado": ["Monrovia", "Paynesville", "St. Paul River", "Bushrod Island"],
        "Nimba": ["Sanniquellie", "Ganta", "Tappita", "Saclepea", "Zoe-Gbao"],
        "Bong": ["Gbarnga", "Salala", "Jorquelleh", "Fuamah"],
        "Lofa": ["Voinjama", "Foya", "Kolahun", "Zorzor"],
        "Grand Bassa": ["Buchanan", "Cestos City", "Owensgrove", "Greenville"],
        "Margibi": ["Kakata", "Firestone", "Cotton Tree", "Harbel"],
        "Bomi": ["Tubmanburg", "Klay", "Senjeh"],
        "Grand Cape Mount": ["Robertsport", "Porkpa", "Gola Konneh"],
        "Gbarpolu": ["Bopolu", "Belleh", "Kongba"],
        "Grand Gedeh": ["Zwedru", "Tchien", "Konobo"],
        "River Gee": ["Fish Town", "Chedepo", "Barclayville"],
        "Sinoe": ["Greenville", "Dugbe River", "Juarzon"],
        "Maryland": ["Harper", "Pleebo", "Karlu"],
        "Rivercess": ["Cestos", "Zammi", "Doe River"],
        "Grand Kru": ["Barclayville", "Sasstown", "Tuzon"],
    }

    for county_name, districts in data.items():
        county, _ = County.objects.get_or_create(name=county_name)
        for district_name in districts:
            District.objects.get_or_create(county=county, name=district_name)