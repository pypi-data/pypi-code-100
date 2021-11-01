from django.apps import apps
from django.core.management.base import BaseCommand, CommandError

from census import Census

from djplacedata.models import Place
from djplacedata.settings import CENSUS_API_KEY, CENSUS_DATASET, CENSUS_YEAR
from djplacedata.utils import get_place_field_from_model, get_census_values_from_model


STATE_GEOIDS = [
    '01', '02', '04', '05', '06', '08', '09', '10', '11',
    '12', '13', '15', '16', '17', '18', '19', '20', '21',
    '22', '23', '24', '25', '26', '27', '28', '29', '30',
    '31', '32', '33', '34', '35', '36', '37', '38', '39',
    '40', '41', '42', '44', '45', '46', '47', '48', '49',
    '50', '51', '53', '54', '55', '56',
]


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('app_label')
        parser.add_argument('model_name',)
        parser.add_argument(
            '--year',
            type=int,
            default=CENSUS_YEAR)
        parser.add_argument(
            '--dataset',
            default=CENSUS_DATASET
        )

    def handle(self, *args, **options):
        app_label = options['app_label']
        model_name = options['model_name']
        year = options['year']
        dataset = options['dataset']

        self.model = apps.get_model(app_label, model_name)
        self.field = get_place_field_from_model(self.model)
        self.values = get_census_values_from_model(self.model)
        self.variables = self.values.variables

        census = Census(CENSUS_API_KEY, year=year)
        self.client = getattr(census, dataset)

        self._import_state_data()
        self._import_county_data()
        self._import_city_data()

    def _import_state_data(self):
        results = self.client.get(self.variables, {
            'for': 'state:*'
        })
        self._create_objects_from_results(results, lambda result: result['state'])

    def _import_county_data(self):
        results = self.client.get(self.variables, {
            'for': 'county:*'
        })
        self._create_objects_from_results(results, lambda result: result['state'] + result['county'])

    def _import_city_data(self):
        for state_geoid in STATE_GEOIDS:
            results = self.client.get(self.variables, {
                'for': 'county subdivision:*',
                'in': 'state:%s' % state_geoid
            })
            self._create_objects_from_results(results, lambda result: result['state'] + result['county'] + result['county subdivision'])

    def _create_objects_from_results(self, results, get_geo_id):
        for result in results:
            try:
                place = Place.objects.get(geoid=get_geo_id(result))
                self.model.objects.update_or_create(
                    **{self.field: place,},
                    defaults=self.values.get_values_from_results(result))
            except Place.DoesNotExist:
                pass
