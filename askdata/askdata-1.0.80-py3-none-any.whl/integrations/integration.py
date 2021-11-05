''' Integration abstract class '''
class Integration():

	def save(self):
		pass

	def load(self):
		pass

	def parse_resultset(json_data):
		# Parse the JSON data
		json_data = json.loads(json_data)
		# Get the data from the JSON
		data = json_data['data']
		# Get the schema from the JSON
		schema = json_data['schema']
		# Create a list of column names
		column_names = [column['name'] for column in schema]
		# Create a list of data
		data_list = [row['cells'] for row in data]
		# Create a dataframe from the data
		df = pd.DataFrame(data_list, columns=column_names)
		# Return the dataframe
		return df

	def return_resultset(df):
		# Get the schema from the dataframe
		schema = df.columns
		# Create a list of dictionaries with the data
		data_list = df.to_dict('records')
		# Create a dictionary with the data
		data = {'data': data_list}
		# Create a dictionary with the schema
		schema_dict = {column: {'name': column} for column in schema}
		# Create a dictionary with the schema and data
		json_dict = {
			'schema': schema_dict,
			'data': data_list,
			'id': None,
			'dataset': {
				'id': '6512cf85-4f81-4fa0-a2b8-c51c6aad6cf9-BIGQUERY-a0fb8755-d50b-412b-9b86-0fd7d5529843',
				'name': 'Datacenters',
				'icon': 'https://storage.googleapis.com/askdata/datasets/icons/icoDataBigQuery.png'
			},
			'connection': '',
			'executedSQLQuery': 'SELECT AVG(`traffic`) AS `alias_0` FROM `askdata.Atlassian.atlassian_datacenter` ORDER BY `alias_0` DESC LIMIT 50',
			'schema': schema_dict,
			'data': data_list,
			'filters': None,
			'sortedBy': None,
			'page': None,
			'limit': 50,
			'totalRecords': 1,
			'queryId': ''
		}
		# Return the dictionary
		return json_dict
