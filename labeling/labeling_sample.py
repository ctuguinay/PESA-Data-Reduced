import random
import os
import csv

def get_paths():
    """
    Get absolute paths to source_five data.csv files.

    Returns:
        uncleaned_combined_path: String that contains the absolute path to the uncleaned source_five data.csv file.
        cleaned_combined_path: String that contains the absolute path to the cleaned source_five data.csv file.
    """

    rel_uncleaned_combined_path = "data/unlabeled/uncleaned/source_five/data.csv"
    rel_cleaned_combined_path = "data/unlabeled/cleaned/source_five/data.csv"
    script_dir = os.path.dirname(__file__)
    uncleaned_combined_path = os.path.join(script_dir, rel_uncleaned_combined_path).replace("\\labeling", "")
    cleaned_combined_path = os.path.join(script_dir, rel_cleaned_combined_path).replace("\\labeling", "")

    return uncleaned_combined_path, cleaned_combined_path

def get_rows(path):
    """
    Get rows from source_five data.csv.

    Args: 
        path: String to indicate path to source_five data.csv.
    """
    
    first_row = ['text', 'source', 'type', 'post_id', 'refer_post_id', 'date']
    rows = [first_row]

    with open(path, 'r', encoding = "utf-8") as unlabeled_file:
        reader = csv.reader(unlabeled_file)
        for index, row in enumerate(reader):
            if index != 0:
                rows.append(row)

    return rows

def sample_rows(rows, sample_amount = 1000):
    """
    Samples from rows.

    Args:
        rows: Array of rows from a data.csv file.
    
    Returns:
        rows: Array of rows from a data.csv file that have been sampled from.
    """

    first_row = ['text', 'source', 'type', 'post_id', 'refer_post_id', 'date']
    sampled_rows = [first_row]
    random.seed(0)
    sampled_rows = sampled_rows + random.sample(rows, sample_amount)

    return sampled_rows

def traverse_new(rows, path):
    """
    Traverse the new data.csv file to place data from a source_five data.csv.

    Args:
        rows: Array that contains data from a source_five data.csv file.
        cleaned_path: String that contains the absolute path to the new data.csv file.
    """

    with open(path, 'w+', encoding = "utf-8", newline= '') as file:
        writer = csv.writer(file)
        for index, row in enumerate(rows):
            writer.writerow(row)

def get_matching(uncleaned_rows, cleaned_rows):
    """
    Gets rows in uncleaned_rows that match with rows in cleaned_rows.

    Args:
        uncleaned_rows: Array that contains data from an uncleaned source_five data.csv file.
        cleaned_rows: Array that contains data from a cleaned source_five data.csv file.

    Returns:
        sampled_uncleaned_rows: Array that contains data from an uncleaned source_five data.csv file that match a sampled cleaned source_five csv file.
    """
    
    sampled_uncleaned_rows = []
    for index, cleaned_row in enumerate(cleaned_rows):
        if index == 0:
            sampled_uncleaned_rows.append(cleaned_row)
        else:
            found = False
            for uncleaned_row in uncleaned_rows:
                if uncleaned_row[1] == cleaned_row[1] and uncleaned_row[2] == cleaned_row[2] and uncleaned_row[3] == cleaned_row[3] and uncleaned_row[3] != None:
                    sampled_uncleaned_rows.append(uncleaned_row)
                    found = True
                    break
            if not found:
                temp_row = cleaned_row
                temp_row[0] = "No Matching."
                sampled_uncleaned_rows.append(temp_row)

    return sampled_uncleaned_rows

if __name__ == "__main__":

    # Sample from cleaned data.
    uncleaned_path, cleaned_path = get_paths()
    cleaned_rows = get_rows(cleaned_path)
    #cleaned_rows = sample_rows(cleaned_rows)
    traverse_new(cleaned_rows, cleaned_path.replace("data.csv", "data_sample.csv"))

    # Get uncleaned rows that correlate with sampled cleaned rows and place it in a CSV.
    uncleaned_rows = get_rows(uncleaned_path)
    sample_uncleaned_rows = get_matching(uncleaned_rows, cleaned_rows)
    traverse_new(sample_uncleaned_rows, uncleaned_path.replace("data.csv", "data_sample.csv"))