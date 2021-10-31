import pandas as pd
import geopandas as gpd
from sklearn.metrics.pairwise import haversine_distances
from math import radians


# COLEÇÃO DE MÉTODOS UTEIS PARA OUTRAS FUNÇÕES DA BIBLIOTECA!

def coord_to_radians(list_coord:list) -> list:
    """
    This function converts coordinates to radians.


    Parameters:
    ----------
    list_coord: list
        receive a list of coordinates.

    Return:
    ------
    list:
        returns a list of tuples containing coordinates in radians.
    """

    coord_in_radians = [tuple([radians(i[0]),radians(i[1])]) for i in list_coord]
    return coord_in_radians
    
def max_dist(coord_in_radians:list) -> float:
    """
    This function receives a list of coordinates in radians and will calculate the greatest distance
    from the midpoint of the coordinates using haversine distance.

    Parameters:
    ----------
    coord_in_radians: list
        coordinate list in radians.
    Return:
    -------
    float: returns a float number representing the greatest distance from the midpoint
    """
    const = 6371000/1000 
    max_dist = round(haversine_distances(coord_in_radians).max()*const,2)
    return max_dist
  
def convertToGeoFormat(df: pd.DataFrame) -> gpd.GeoDataFrame:
    """
    This function transforms a dataframe into a geodataframe using the geometry column.

    Parameters:
    ----------
    df: DataFrame
        dataframe that will be converted

    Errors:
    ------
    RuntimeError: if the dataframe does not have the geometry column
    Return:
    -------
    dispersion_df: gpd.GeoDataFrame
        dataframe resulting from conversion
    """
    
    if isinstance(df.geometry,gpd.GeoSeries):
        new_df = df
    
    elif "geometry" in df.columns:
        df['geometry'] = gpd.GeoSeries.from_wkt(df['geometry'])
        new_df = gpd.GeoDataFrame(df, geometry="geometry")
    elif 'latitude' and 'longitude' in df.columns:
        df['geometry'] = gpd.GeoSeries.from_xy(df.longitude,df.latitude)
        new_df = gpd.GeoDataFrame(df, geometry="geometry")
    else:
        raise RuntimeError("The dataframe needs a column named geometry or a latitude and longitude ones")
    if "Unnamed: 0" in new_df.columns:
        new_df = new_df.drop(columns=["Unnamed: 0"], axis=1)
  
    
    return new_df