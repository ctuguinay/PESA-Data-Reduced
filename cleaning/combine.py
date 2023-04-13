import csv
import os
from helper import traverse_new

def get_paths():
    """
    Get paths to the uncleaned and cleaned file.

    Returns:
        uncleaned_array: Array of strings that contain the absolute path to an uncleaned data.csv.
        cleaned_array: Array of strings that contain the absolute path to a cleaned data.csv.
        uncleaned_combined_path: String that contain the absolute path to a combined uncleaned data.csv.
        cleaned_combined_path: String that contain the absolute path to a combined cleaned data.csv.
    """

    uncleaned_array = []
    cleaned_array = []
    source_array = ["source_one", "source_two", "source_three", "source_four", "source_five"]
    for media_source in source_array:
        rel_uncleaned_path = "data/unlabeled/uncleaned/" + media_source + "/" + "data.csv"
        rel_cleaned_path = "data/unlabeled/cleaned/" + media_source + "/" + "data.csv"
        script_dir = os.path.dirname(__file__)
        uncleaned_path = os.path.join(script_dir, rel_uncleaned_path).replace("\\cleaning", "")
        uncleaned_array.append(uncleaned_path)
        cleaned_path = os.path.join(script_dir, rel_cleaned_path).replace("\\cleaning", "")
        cleaned_array.append(cleaned_path)
    
    rel_uncleaned_combined_path = "data/unlabeled/uncleaned/combined/data.csv"
    rel_cleaned_combined_path = "data/unlabeled/cleaned/combined/data.csv"
    script_dir = os.path.dirname(__file__)
    uncleaned_combined_path = os.path.join(script_dir, rel_uncleaned_combined_path).replace("\\cleaning", "")
    cleaned_combined_path = os.path.join(script_dir, rel_cleaned_combined_path).replace("\\cleaning", "")

    return uncleaned_array, cleaned_array, uncleaned_combined_path, cleaned_combined_path

def traverse_original(array):
    """
    Get data from data.csv file.

    Args:
        array: Array of strings that contain the absolute path to a data.csv file.

    Returns:
       rows: Array that contains data from multiple uncleaned data.csv files.
    """

    first_row = ['text', 'source', 'type', 'post_id', 'refer_post_id', 'date']
    rows = [first_row]

    for path in array:
        with open(path, 'r', encoding = "utf-8") as unlabeled_file:
            reader = csv.reader(unlabeled_file)
            for index, row in enumerate(reader):
                if index != 0:
                    rows.append(row)
    
    return rows

if __name__ == "__main__":
    
    # Get paths.
    uncleaned_array, cleaned_array, uncleaned_combined_path, cleaned_combined_path = get_paths()

    # Get uncleaned data.
    uncleaned_rows = traverse_original(uncleaned_array)

    # Combine uncleaned data.
    traverse_new(uncleaned_rows, uncleaned_combined_path)

    # Get cleaned data.
    cleaned_rows = traverse_original(cleaned_array)

    # Combine cleaned data.
    traverse_new(cleaned_rows, cleaned_combined_path)