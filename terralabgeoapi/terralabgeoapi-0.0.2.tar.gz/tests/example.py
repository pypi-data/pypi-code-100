import Geocoding
import geopandas as gpd
from geopandas.tools import geocoding
import pandas as pd

providers = {'herev7': {
                    'config': {
                           'apikey':'5DdXY9EzPg6OLnPfhpXHCb3KTlFLiA8Hea1bRnBMXLk'},
                    'countries': ['BRA']},
                    
             'mapbox': {
                    'config': {
                           'api_key':'pk.eyJ1IjoibHVjYXNuYXRhbGk5OCIsImEiOiJja3F2OGd3ZmEwYzFqMzBydTl3M2U2bzUzIn0.XrzgU1YtgRh6kr6c3o7BVA'},
                    'country': 'BR'},

             'tomtom': {
                    'config': {
                           'api_key':'t1jHz8RCZJfbUTZygy5Wac7UaXP5vJTX',
                           'timeout':982},
                    'language': 'pt-BR'},

             'google': {
                    'config': {
                           'domain':'maps.google.com.br',
                           'api_key':'AIzaSyAnJfHQRB9x4DLZyC5_6WIvawPTwVVbFqg'},
                    'region': 'br'},

             'nominatim': {
                    'config': {
                           'user_agent':'alan.ufop@gmail.com'},
                    'country_codes': 'br'},

              'Pelias': {
                    'config': {
                           'domain':'54.236.46.102:8000',
                           'scheme':'http'},
                    'country_bias': 'BRA'}}



data = pd.read_csv('id29-clientes-mapeado_consolidado.csv', sep=';',
                   encoding='latin-1', usecols=['end_completo', 'longitude', 'latitude'])

geo_data = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(
    data.longitude, data.latitude)).sample(n=100, random_state=1)

end = geo_data['end_completo']
cord = geo_data.geometry

dataframe = gpd.GeoDataFrame()
for provider, configs in providers.items():
    df = Geocoding.geocode(end, provider=provider, **configs)
    dataframe = pd.concat([dataframe,df],axis=0,)

dataframe.to_csv('data.csv')
