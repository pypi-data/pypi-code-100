# %% Support for spinners
from yaspin import yaspin

# %% Source: https://public.opendatasoft.com/explore/dataset/geonames-all-cities-with-a-population-1000
import pandas as pd

print('TOP 100 MOST POPULOUS CITIES BY COUNTRY')

with yaspin(text='Downloading cities and population dataset') as sp:
    # WARNING: Requires an active internet connection
    # WARNING: May take some time as this is a very large file!
    cities = pd.read_csv('https://public.opendatasoft.com/explore/dataset/geonames-all-cities-with-a-population-1000/download/?format=csv&timezone=Europe/Berlin&lang=en&use_labels_for_header=true&csv_separator=%3B',  # noqa: E501
                         sep=';')[['Geoname ID', 'Name', 'ASCII Name', 'Alternate Names', 'Country Code', 'Population']]
    sp.ok('✔')

with yaspin(text='Preparing data') as sp:
    cities.columns = cities.columns.map(lambda x: str.lower(x).replace(' ', '_'))
    cities['country_code'] = cities['country_code'].str.lower()
    cities = cities.sort_values('population', ascending=False).groupby('country_code').head(100)[['country_code',
                                                                                                  'name',
                                                                                                  'ascii_name',
                                                                                                  'alternate_names',
                                                                                                  'population']]
    sp.ok('✔')

filename = 'top_100_cities.csv'

with yaspin(text=f'Writing to "{filename}"') as sp:
    cities.to_csv(filename, sep=';', index=False)
    sp.ok('✔')


# %%
