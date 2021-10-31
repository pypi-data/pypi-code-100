from visualization import visualize_dispersion
import pandas as pd

df = pd.read_csv('GeoAPI/Data/out.csv')
visualize_dispersion(df)
#example
from GeoAPI.visualization import *
from GeoAPI.point_validation import batch_outside_geometry_limits
from GeoAPI.preprocessing import *
from pkg_resources import resource_filename

df = pd.read_csv(resource_filename('GeoAPI','Data/data2.csv'))
gs = pd.read_csv(resource_filename('GeoAPI', 'Data/id29-clientes-mapeado_consolidado.csv'), sep=";",
                encoding="latin-1")
print(df.columns)

plot_coordinates(df, hover_data=None)

visualizeByGeocodeService(df, hover_data=None, 
            address_column="end_completo",hover_name=None)

df2 = splitFullAddress(df)

new_df = batch_outside_geometry_limits(df2)

visualizeOutsidePoints(new_df, column_color="outside", hover_name=None, hover_data=None)

disp_df = get_dispersion(new_df, metrics=["DistanceFromMean"])

visualize_dispersion(disp_df, hover_name=None, hover_data=None, 
                    metric="DistanceFromMean")

