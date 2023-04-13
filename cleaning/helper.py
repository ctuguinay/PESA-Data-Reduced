import emoji
import datetime
import csv
import re
import pandas as pd

def replace_emojis(string):
    """
    Converts all emojis to words.

    Args:
        string: String that is going to be modified.

    Returns:
        string: String that has been modified.
    """

    old_string = string
    string = emoji.demojize(string)
    if old_string.count("face") < string.count("face"):
        string = string.replace("face", "")
    string = string.replace(":", " ")
    string = string.replace("_", " ")

    return string

def utc_seconds_to_datetime(utc_seconds):
    """
    Converts utc seconds to datetime string

    Args:
        utc_seconds: Float or int that is to be modified.

    Returns:
        datetime_string: String that has been modified.
    """

    datetime_string = datetime.datetime.fromtimestamp(utc_seconds).strftime('%Y-%m-%d %H:%M:%S')
    return datetime_string

def traverse_new(rows, path):
    """
    Traverse the new data.csv file to place data from another data.csv.

    Args:
        rows: Array that contains data from another data.csv file or multiple data.csv files.
        cleaned_path: String that contains the absolute path to the new data.csv file.
    """

    with open(path, 'w+', encoding = "utf-8", newline= '') as file:
        writer = csv.writer(file)
        for index, row in enumerate(rows):
            writer.writerow(row)

def remove_duplicates(cleaned_path):
    """
    Removes duplicate rows in a CSV.

    Args:
        cleaned_path: String that contains the absolute path to the cleaned data.csv.
    """

    # Read CSV.
    data_frame = pd.read_csv(cleaned_path)

    # For complete row duplicate.
    data_frame.drop_duplicates(inplace=True)
                
    # For partials.
    data_frame.drop_duplicates(subset=['post_id'], inplace=True)

    # Save it.
    data_frame.to_csv(cleaned_path, index=False)


def remove_duplicate_text(cleaned_path):
    """
    Removes duplicate rows in a CSV (by text).

    Args:
        cleaned_path: String that contains the absolute path to the cleaned data.csv.
    """

    # Read CSV.
    data_frame = pd.read_csv(cleaned_path)
                
    # For partials.
    data_frame.drop_duplicates(subset=['text'], inplace=True)

    # Save it.
    data_frame.to_csv(cleaned_path, index=False)


def general_text_cleaning(text):
    """
    Applies general text cleaning to a string.

    Args:
        text: String that is to be cleaned.

    Returns:
        text: String that has been cleaned.
    """

    # Lowercase Text.
    text = text.lower()

    # Remove Hyperlinks.
    text = re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
    text = re.sub(r'http\S+', '', text)

    # Remove all Non-Alphabet Characters except for Spaces.
    regex = re.compile('[^a-zA-Z\s]')
    text = regex.sub('', text)

    # Remove multiple whitespaces.
    text = ' '.join(text.split())

    return text