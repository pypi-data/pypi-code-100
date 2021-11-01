from django.conf import settings


CENSUS_API_KEY = getattr(settings, 'CENSUS_API_KEY', None)
CENSUS_YEAR = getattr(settings, 'CENSUS_YEAR', 2019)
CENSUS_DATASET =  getattr(settings, 'CENSUS_DATASET', 'acs5')
CENSUS_SHAPEFILE_SIMPLIFICATION  = getattr(settings, 'CENSUS_SHAPEFILE_SIMPLIFICATION', 0.0005)
