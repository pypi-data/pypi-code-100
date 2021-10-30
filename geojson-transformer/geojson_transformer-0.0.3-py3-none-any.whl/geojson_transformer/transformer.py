import os
import csv
import json
from lxml import etree
from utils.geo_utils import haversine
import json


class GeoJsonTransformer():
    """A class to represent geo location object from GPX file.

    Provides functionality to extract data from a GPX file.
    A GPX file can be transformed to a GeoJson object.
    """

    CONFIG_JSON_PATH = 'src/geojson_transformer/config.json'

    def __init__(self, path=None, in_memory_file=None):
        self.path = path
        self.file = in_memory_file
        self.parser = etree.XMLParser(remove_blank_text=True)
        self.json_data = None
        self._name = None
        self._coordinates_list = None
        self._elevations_list = None
        self._total_distance = None
        self._total_elevation = None
        self._ele_distance_pairs = None
        self._starting_point = None
        self._paired_data = None

        self.prepare_data = self.setup_lists() if path or in_memory_file else None


    @property
    def name(self):
        if self._name:
            return self._name
        if self.path:
            self._name = os.path.basename(self.path).split('.')[-2]
            return self._name
        elif self.file:
            self._name = os.path.basename(self.file.name).split('.')[-2]
            return self._name

    @property
    def root(self):
        return self.tree.getroot()
    
    @property
    def tree(self):
        if self.path:
            with open(self.path, 'r') as f:
                tree = etree.parse(f, self.parser)
                tree = self.strip_ns_prefix(tree)
            return tree
        elif self.file:
            tree = etree.parse(self.file, self.parser)
            tree = self.strip_ns_prefix(tree)
            return tree

    def strip_ns_prefix(self, tree):
        #xpath query for selecting all element nodes in namespace
        query = "descendant-or-self::*[namespace-uri()!='']"
        #for each element returned by the above xpath query...
        for element in tree.xpath(query):
            #replace element name with its local name
            element.tag = etree.QName(element).localname
        return tree

    @property
    def coordinates_list(self):
        """Returns a list of lon, lat data."""
        
        if self._coordinates_list:
            return self._coordinates_list

        coordinates_list = []
        for element in self.root.iter('trkpt'):
            lon = float(element.attrib.get('lon'))
            lat = float(element.attrib.get('lat'))
            coordinates_list.extend([lon, lat])
        self._coordinates_list = coordinates_list
        return self._coordinates_list

    @property
    def elevation_list(self):
        """Returns a list of object elevation data."""

        if self._elevations_list:
            return self._elevations_list

        elevations_list = []
        for element in self.root.iter('trkpt'):
            ele = element.findtext('ele')
            if ele:
                elevations_list.append(float(ele))
        self._elevations_list = elevations_list
        return self._elevations_list

    @property
    def paired_data(self):
        """Returns the object data paired in a list of (lat, lon, elevation) pairs."""

        if self._paired_data:
            return self._paired_data
        elevations_list = self.elevation_list
        coordinates_list = self.coordinates_list
        self._paired_data = [list(z) for z in zip(coordinates_list[::2], coordinates_list[1::2], elevations_list)]
        return self._paired_data

    @property
    def ele_distance_pairs(self):
        """Returns list of elevation, distance pairs where each tuple contains
           current elevation and total distance up to that point.
        """
        if self._ele_distance_pairs:
            return self._ele_distance_pairs

        cl = self.coordinates_list
        lines = list(zip(cl[::2], cl[1::2], cl[2::2], cl[3::2]))
        distance_steps = [0]
        for line in lines:
            distance_steps.append(distance_steps[-1] + haversine(line[0], line[1], line[2], line[3]))            
        return list(zip(distance_steps, self.elevation_list))

    def _make_geojson(self):
        with open(self.CONFIG_JSON_PATH) as f:
            schema = json.load(f)
            schema["features"][0]["properties"]["name"] = self.name
            schema["features"][0]["geometry"]["coordinates"].extend(self.paired_data)
            self.json_data = schema
        return schema
    
    @property
    def total_elevation(self):
        """Returns the total positive gain in elevation as an int."""

        if self._total_elevation:
            return self._total_elevation

        el = self.elevation_list
        total_elevation = 0
        elevation_pairs = list(zip(el[0:], el[1:]))
        for e in elevation_pairs:
            if e[1] > e[0]:
                diff = e[1]-e[0]
                total_elevation += diff
        self._total_elevation = int(total_elevation)
        return self._total_elevation

    @property
    def total_distance(self):
        """Returns the sum between all coordinate points in the object."""

        if self._total_distance:
            return self._total_distance

        cl = self.coordinates_list
        total_distance = 0
        lines = list(zip(cl[::2], cl[1::2], cl[2::2], cl[3::2]))
        for line in lines:
            total_distance += haversine(line[0], line[1], line[2], line[3])
        self._total_distance = round(total_distance, 2)
        return self._total_distance

    @property
    def starting_point(self):
        """Returns the first lat/lon pair found in the object."""

        if self._starting_point:
            return self._starting_point

        self._starting_point = (self.coordinates_list[0], self.coordinates_list[1])
        return self._starting_point

    def save_geojson(self, filepath=None):
        """Creates a GeoJson file at the specified filepath. Returns the object as json."""
        if not filepath:
            filepath = self.name + '.json' # TODO: find a better way for that
        filepath = filepath.split('.')
        filepath[-1] = 'json'
        filepath = '.'.join(filepath)
        
        with open(filepath, 'w') as outfile:
            json.dump(self._make_geojson(), outfile)
            return outfile

    def to_csv(self, filepath=None):
        """
        Creates a csv file that has two rows 'elevation' and 'distance'.
        Each row has the current elevation and total distance up to that point.        
        """
        if not filepath:
            filepath = self.name + '.csv' # TODO: find a better way for that
        filepath = filepath.split('.')
        filepath[-1] = 'csv'
        filepath = '.'.join(filepath)

        with open(filepath, 'w', newline='') as csvfile:
            eledistancewriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            eledistancewriter.writerow(['distance', 'elevation'])
            for pair in self.ele_distance_pairs:
                eledistancewriter.writerow([round(pair[0], 2), round(pair[1], 2)])
        if csvfile:
            return csvfile
        return None
        


    def setup_lists(self):
        """Loads up initial data into the object."""

        if self.file:
            self.coordinates_list
            self.file.seek(0)
            self.elevation_list
            self.file.seek(0)
            
        elif self.path:
            self.coordinates_list
            self.elevation_list
