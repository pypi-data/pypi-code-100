from GeoAPI import Geocoding
import geopandas as gpd
import pandas as pd

providers = {

             'google': {
                    'config': {
                           'domain':'maps.google.com.br',
                           'api_key':'AIzaSyAnJfHQRB9x4DLZyC5_6WIvawPTwVVbFqg'},
                    'region': 'br'}}



data = pd.read_csv('/home/alanss/ml/Data Analytics - TerraLAB/GeoAPI - library/GeoAPI/Data/id29-clientes-mapeado_consolidado.csv', sep=';',
                   encoding='latin-1', usecols=['end_completo', 'longitude', 'latitude'])

geo_data = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(
    data.longitude, data.latitude)).sample(n=5, random_state=1)

end = geo_data['end_completo']
cord = geo_data.geometry

dataframe = gpd.GeoDataFrame()
for provider, configs in providers.items():
    df,_ = Geocoding.geocode(end, provider=provider, **configs)
    dataframe = pd.concat([dataframe,df],axis=0,)

dataframe.to_csv('data.csv')
