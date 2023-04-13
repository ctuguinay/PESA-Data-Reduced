import pytest
import csv
import os

@pytest.fixture
def initialize_paths():
    """
    Gets the paths to the files modified by /cleaning.
    
    Returns:
        results: Array containing strings for the absolute paths to the target files.
    """
    
    rel_search_path = "/data/unlabeled/cleaned/"
    dir_path_appended = os.path.dirname(__file__) + rel_search_path
    abs_search_path = dir_path_appended.replace("\\cleaning\\tests", "")
    paths = []
    for root, dir, files in os.walk(abs_search_path):
        for filename in files:
            if filename.endswith("data.csv"):
                if "/combined" in filename:
                    paths.append(os.path.join(root, filename.replace("cleaned", "uncleaned")))
                paths.append(os.path.join(root, filename))

    return paths

def test_structures(initialize_paths):
    """
    Tests the structure of the data.csv and/or similarly named files modified or added to by /cleaning.

    Args:
        initialize_paths: Array containing strings for the absolute paths to the target files.
    """

    paths = initialize_paths
    for path in paths:
        assert isinstance(path, str)
        with open(path, 'r', encoding = "utf-8") as file:
            reader = csv.reader(file)
            for row_index, row in enumerate(reader):
                if row_index == 0:
                    assert row == ['text', 'source', 'type', 'post_id', 'refer_post_id', 'date']
                else:
                    for item_index, item in enumerate(row):
                        if item_index == 1:
                            assert item == "source_one" or item == "source_two" or item == "source_three" or item == "source_four" or item == "source_five"
                        elif item_index == 3 or item_index == 4:
                            assert item == "None" or item.isnumeric()
                        assert isinstance(item, str)