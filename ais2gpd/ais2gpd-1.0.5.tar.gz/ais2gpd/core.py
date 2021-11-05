import geopandas as gpd
import pandas as pd
import requests
from pkg_resources import packaging

GEOPANDAS_VERSION = packaging.version.parse(gpd.__version__)

API_ENDPOINT = "http://api.phila.gov/ais/v1"


def get(addresses, ais_key, fields=None, params={}):
    """
    Query the AIS API, returning a GeoDataFrame.

    More information on AIS API usage can be found here:
    https://github.com/CityOfPhiladelphia/ais/blob/master/docs/APIUSAGE.md

    Parameters
    ----------
    addresses : list, pandas.Series
        the list of addresses to get information for
    ais_key : str
        the AIS API key for authentication purposes
    fields : list of str, optional
        the name of the fields to return; the default behavior returns
        all fields
    params : dict
        additional query parameters to provide

    Example
    -------
    >>> import ais2gpd
    >>> import os
    >>> ais_key = os.environ['AIS_API_KEY']
    >>> gdf = ais2gpd.get(['1234 market st', '945 N 5th st'], ais_key, fields=['zip_code', 'police_district'])
    >>> gdf
    """
    params["gatekeeperKey"] = ais_key

    def get_single_query(address):
        url = f"{API_ENDPOINT}/search/{address}"
        r = requests.get(url, params=params)
        json = r.json()
        if json.get("total_size", 0) > 0:
            return json["features"][0]
        else:
            return {"geometry": None, "properties": []}

    # query the endpoint for each ro
    if isinstance(addresses, list):
        addresses = pd.Series(addresses)
    features = addresses.apply(get_single_query)

    # create the GeoDataFrame with the proper EPSG code
    srid = params.get("srid", 4326)

    # Convert to a GeoDataFrame
    if GEOPANDAS_VERSION >= packaging.version.parse("0.7"):
        toret = gpd.GeoDataFrame.from_features(features, crs=f"EPSG:{srid}")
    else:
        toret = gpd.GeoDataFrame.from_features(features, crs={"init": f"epsg:{srid}"})

    # Return the proper fields
    if isinstance(fields, (tuple, list)) and len(fields) > 0:
        fields = [col for col in fields if col in toret.columns]
        if "geometry" not in fields:
            fields += ["geometry"]
        toret = toret[fields]

    return toret
