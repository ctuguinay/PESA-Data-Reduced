from helper import replace_emojis, general_text_cleaning, traverse_new, remove_duplicate_text
import csv
import os

def get_paths():
    """
    Get paths to the uncleaned and cleaned file.

    Returns:
        uncleaned_path: String that contains the absolute path to the uncleaned data.csv.
        cleaned_path: String that contains the absolute path to the cleaned data.csv.
    """

    media_source = os.path.basename(__file__).replace(".py", "")
    rel_uncleaned_path = "data/unlabeled/uncleaned/" + media_source + "/" + "data.csv"
    rel_cleaned_path = "data/unlabeled/cleaned/" + media_source + "/" + "data.csv"
    script_dir = os.path.dirname(__file__)
    uncleaned_path = os.path.join(script_dir, rel_uncleaned_path).replace("\\cleaning", "")
    cleaned_path = os.path.join(script_dir, rel_cleaned_path).replace("\\cleaning", "")

    return uncleaned_path, cleaned_path

def traverse_original(uncleaned_path):
    """
    Get paths to the uncleaned and cleaned file.

    Args:
        uncleaned_path: String that contains the absolute path to the uncleaned data.csv.

    Returns:
        rows: Array that contains data from an uncleaned data.csv file.
    """

    rows = []
    with open(uncleaned_path, 'r', encoding = "utf-8") as unlabeled_file:
        reader = csv.reader(unlabeled_file)
        for index, row in enumerate(reader):
            mod_text = row[0]
            mod_text = replace_emojis(mod_text)
            mod_text = general_text_cleaning(mod_text)
            row[0] = mod_text
            rows.append(row)
    
    return rows


if __name__ == "__main__":

    # Get Paths.
    uncleaned_path, cleaned_path = get_paths()

    # Get Rows.
    rows = traverse_original(uncleaned_path)

    # Place Rows in the Absolute Cleaned Path.
    traverse_new(rows, cleaned_path)

    # Remove duplicates.
    remove_duplicate_text(cleaned_path)