"""module responsible for testing data ingest """
import os


def test_data_raw_path():
    """
    Asserting data raw path
    """

    expected_path = os.path.abspath(os.path.join(os.getcwd(), "data/raw"))

    assert expected_path == '/home/matheus/Documentos/repos/refactor_rossmann/data/raw'
