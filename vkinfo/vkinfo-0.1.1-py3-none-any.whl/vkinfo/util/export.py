import logging
import pandas as pd


class Exporter(object):
    """Exporter class for ease of use and expansion

    Args:
        dataframe: pandas dataframe to save/export/freeze etc.
    """
    def __init__(self,
                 dataframe: pd.DataFrame
                 ) -> None:

        self.dataframe = dataframe

    def save(self,
             export_path: str,
             export_format: str) -> None:
        """Write dataframe to file w/ desired format

        Args:
            export_path: Path to export file.
            export_format: Export file format [csv, tsv, json, etc.]
        """
        if export_format == "csv":
            logging.info("Saving data in '.csv' format")

            self.dataframe.to_csv(f'{export_path}.csv', index=False)

        elif export_format == "json":
            logging.info("Saving data in '.json' format")

            self.dataframe.to_json(f'{export_path}.json', orient='records',
                            force_ascii=False, indent=2)

        elif export_format == "tsv":
            logging.info("Saving data in '.tsv' format")

            self.dataframe.to_csv(f'{export_path}.tsv', index=False, sep='\t')

        logging.info(f"Exported as {export_path}.{export_format}")
