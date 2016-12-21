import csv
import os
from django.conf import settings
from datanalyse.models import BuyStockTable
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def handle(self, *args, **options):
        print "Loading CSV"
        csv_path = os.path.join(settings.BASE_DIR, "/home/ashraydimri/Downloads/graphweb/ListOfScrips2.csv")
        csv_file = open(csv_path, 'rb')
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            obj = BuyStockTable.objects.create(
                ticker=row['Ticker'],
                name=row['Name']
            )
