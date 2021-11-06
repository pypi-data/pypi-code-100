import json
import click

@click.command()
@click.option('--input', '-i', help='path to input file', required=True)
@click.option('--output', '-o', help='path to outpu file', required=True)
def format(input, output):
	input_data = json.loads(open(input, 'r', encoding='utf-8').read())

	features = input_data.get('features')

	del input_data["features"]

	metadata = json.dumps(input_data, ensure_ascii=False)[:-1]

	with open(output, 'w', encoding='utf-8') as file_w:
		file_w.write('{},"features":[\n'.format(metadata))
		had_first = False
		for feature in features:
			if had_first:
				file_w.write(",\n")
			else:
				had_first = True
			file_w.write(json.dumps(feature))

		file_w.write('\n]}')

if __name__ == "__main__":
	format()
