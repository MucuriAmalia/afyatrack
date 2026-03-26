from django.core.management.base import BaseCommand
from core.models import Country, County, SubCounty, Ward

# Partial Kenya data with sub-counties and wards (fill in others later)
KENYA_DATA = {
    "Nairobi": {
        "Westlands": ["Kitisuru", "Parklands/Highridge", "Karura", "Kangemi", "Mountain View"],
        "Dagoretti North": ["Kilimani", "Kawangware", "Gatina", "Kileleshwa", "Kabiro"],
        "Dagoretti South": ["Mutuini", "Ngando", "Riruta", "Uthiru/Ruthimitu", "Waithaka"],
        "Langata": ["Karen", "Nairobi West", "Mugumoini", "South C", "Nyayo Highrise"],
        "Kibra": ["Laini Saba", "Lindi", "Makina", "Woodley/Kenyatta Golf", "Sarang'ombe"],
        "Roysambu": ["Githurai", "Kahawa West", "Zimmerman", "Roysambu", "Kahawa"],
        "Kasarani": ["Clay City", "Mwiki", "Kasarani", "Njiru", "Ruai"],
        "Ruaraka": ["Baba Dogo", "Utalii", "Mathare North", "Lucky Summer", "Korogocho"],
        "Embakasi South": ["Kwa Njenga", "Imara Daima", "Kware", "Kwa Reuben", "Pipeline"],
        "Embakasi North": ["Kariobangi North", "Dandora Area I", "Dandora Area II", "Dandora Area III", "Dandora Area IV"],
        "Embakasi Central": ["Kayole North", "Kayole Central", "Kayole South", "Komarock", "Matopeni/Spring Valley"],
        "Embakasi East": ["Upper Savannah", "Lower Savannah", "Embakasi", "Utawala", "Mihango"],
        "Embakasi West": ["Umoja I", "Umoja II", "Mowlem", "Kariobangi South"],
        "Makadara": ["Maringo/Hamza", "Viwandani", "Harambee", "Makongeni", "South B"],
        "Kamukunji": ["Pumwani", "Eastleigh North", "Eastleigh South", "Airbase", "California"],
        "Starehe": ["Nairobi South", "Nairobi Central", "Ngara", "Pangani", "Landimawe", "Ziwani/Kariokor"],
        "Mathare": ["Mabatini", "Huruma", "Ngei", "Mlango Kubwa", "Kiamaiko", "Hospital"],
    },
    "Kwale": {
        "Lunga Lunga": ["Vanga", "Mwereni", "Dzombo", "Pongwe/Kikoneni"],
        "Msambweni": ["Ukunda", "Kinondo", "Gombato Bongwe", "Ramisi"],
        "Matuga": ["Mkongani", "Tiwi", "Kubo South", "Waa", "Tsimba Golini"],
        "Kinango": ["Mwavumbo", "Chengoni/Samburu", "Kasemeni", "Mackinon Road", "Kinango", "Puma", "Ndavaya"],
    },
    "Kilifi": {
        "Kilifi North": ["Tezo", "Sokoni", "Kibarani", "Dabaso", "Matsangoni", "Watamu", "Mnarani"],
        "Kilifi South": ["Junju", "Mwarakaya", "Shimo la Tewa", "Chasimba", "Mtepeni"],
        "Malindi": ["Jilore", "Kakuyuni", "Ganda", "Malindi Town", "Shella"],
        "Magarini": ["Maarafa", "Magarini", "Gongoni", "Adu", "Garashi", "Sabaki"],
        "Rabai": ["Rabai/Kisurutuni", "Mwawesa", "Kambe/Ribe", "Ruruma", "Jibana"],
        "Ganze": ["Jaribuni", "Sokoke", "Ganze", "Vitengeni", "Bamba", "Dungicha"],
    },
    "Taita-Taveta": {
        "Taveta": ["Chala", "Mahoo", "Bomani", "Mboghoni", "Mata"],
        "Wundanyi": ["Wundanyi/Mbale", "Werugha", "Wumingu/Kishushe", "Mwanda/Mgange"],
        "Mwatate": ["Ronge", "Mwatate", "Bura", "Chawia", "Wusi/Kishamba"],
        "Voi": ["Mbololo", "Kaloleni", "Sagala", "Marungu", "Kasigau", "Ngolia"],
    },
    "Mombasa": {
        "Changamwe": ["Port Reitz", "Kipevu", "Airport", "Miritini", "Chaani"],
        "Jomvu": ["Jomvu Kuu", "Magongo", "Mikindani"],
        "Kisauni": ["Mjambere", "Junda", "Bamburi", "Mwakirunge", "Mtopanga", "Magogoni", "Shanzu"],
        "Nyali": ["Frere Town", "Ziwa La Ng’ombe", "Mkomani", "Kongowea", "Kadzandani"],
        "Likoni": ["Mtongwe", "Shika Adabu", "Bofu", "Likoni", "Timbwani"],
        "Mvita": ["Mji wa Kale/Makadara", "Tudor", "Tononoka", "Shimanzi/Ganjoni", "Majengo"],
    },
    # Add other counties with empty dicts for now
    "Baringo": {},
    "Bomet": {},
    "Bungoma": {},
    "Busia": {},
    "Elgeyo-Marakwet": {},
    "Embu": {},
    "Garissa": {},
    "Homa Bay": {},
    "Isiolo": {},
    "Kajiado": {},
    "Kakamega": {},
    "Kericho": {},
    "Kiambu": {},
    "Kirinyaga": {},
    "Kisii": {},
    "Kisumu": {},
    "Kitui": {},
    "Laikipia": {},
    "Lamu": {},
    "Machakos": {},
    "Makueni": {},
    "Mandera": {},
    "Marsabit": {},
    "Meru": {},
    "Migori": {},
    "Murang'a": {},
    "Nakuru": {},
    "Nandi": {},
    "Narok": {},
    "Nyamira": {},
    "Nyandarua": {},
    "Nyeri": {},
    "Samburu": {},
    "Siaya": {},
    "Tana River": {},
    "Tharaka-Nithi": {},
    "Trans Nzoia": {},
    "Turkana": {},
    "Uasin Gishu": {},
    "Vihiga": {},
    "Wajir": {},
    "West Pokot": {},
}

class Command(BaseCommand):
    help = "Load Kenya with counties, sub-counties, and wards"

    def handle(self, *args, **kwargs):
        kenya, _ = Country.objects.get_or_create(name="Kenya")

        for county_name, subcounties in KENYA_DATA.items():
            county, _ = County.objects.get_or_create(name=county_name, country=kenya)
            for subcounty_name, wards in subcounties.items():
                subcounty, _ = SubCounty.objects.get_or_create(name=subcounty_name, county=county)
                for ward_name in wards:
                    Ward.objects.get_or_create(name=ward_name, subcounty=subcounty)

        self.stdout.write(self.style.SUCCESS("Kenya counties, sub-counties, and wards loaded successfully"))