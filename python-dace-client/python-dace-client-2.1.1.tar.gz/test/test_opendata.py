import os
import pytest
from pathlib2 import Path
from dace import DaceClass
from dace.opendata import OpenDataClass


@pytest.fixture(scope='module')
def opendata_without_dace_authentication():
    dace = DaceClass(config_path=Path(str(Path(__file__).parent) + os.sep + 'config.ini'))
    return OpenDataClass(dace_instance=dace)


def test_should_query_opendata_database(opendata_without_dace_authentication):
    publications = opendata_without_dace_authentication.query_database(limit=10)
    assert all(
        key in publications.keys() for key in
        ['main_project_label', 'main_project_leader', 'project_label', 'project_leader', 'pub_first_author',
         'pub_title', 'pub_date', 'pub_journal', 'pub_bibcode', 'pub_doi', 'pub_openaccess_url',
         'data_dace_id', 'data_license', 'data_dace_archive_path', 'data_dace_readme_path',
         'data_external_repositories', 'pub_all_authors', 'data_status', 'user_id', 'ads_link', 'doi_link',
         'pub_referred', 'pub_major'])
    for data_external_repositories in publications['data_external_repositories']:
        assert isinstance(data_external_repositories, list)
    for pub_majors in publications['pub_major']:
        assert isinstance(pub_majors, list)
        for pub_major in pub_majors:
            assert isinstance(pub_major, bool)


@pytest.mark.skip(reason="To activate when fixed data with real publications are present")
def test_should_download_opendata_readme(opendata_without_dace_authentication):
    expected_file = '/tmp/Readme.md'
    opendata_without_dace_authentication.download('DACE-OD-2019ASPC..523..405B', 'readme', output_directory='/tmp',
                                                  output_filename='Readme.md')
    assert Path(expected_file).exists() is True
