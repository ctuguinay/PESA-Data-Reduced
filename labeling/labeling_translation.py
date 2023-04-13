from googletrans import Translator
import csv
import os

def initialize_paths():
    """
    Initialize relevant paths to to-be translated data and translated data.

    Returns:
        abs_unlabeled_path: String for unlabeled path to data.
        abs_translated_path: String for translated path to data.
    """

    # Get relevant paths.
    rel_data_path = "data/unlabeled/cleaned/source_five/data_sample.csv"
    script_dir = os.path.dirname(__file__)
    abs_unlabeled_path = os.path.join(script_dir, rel_data_path).replace("labeling\\", "")

    # Check that abs_unlabeled_path exists.
    if not os.path.exists(abs_unlabeled_path):
        raise ValueError(f"There exists no data.csv within {abs_unlabeled_path}.")

    # Get target labeled path location.
    abs_translated_path = os.path.join(script_dir, rel_data_path).replace("labeling\\", "")
    abs_translated_path = abs_translated_path.replace("data_sample.csv", "data_sample_translated.csv")

    return abs_unlabeled_path, abs_translated_path

def initialize_data(abs_unlabeled_path):
    """
    Grab data from unlabeled file.

    Args:
        abs_path: String for path to unlabeled data.
        make_new_labeled: Boolean to make new labeled dataset or to use existing data.

    Returns:
        labeled_data: Array that contains unlabeled data.
    """

    unlabeled_data = []
    with open(abs_unlabeled_path, 'r', encoding = "utf-8") as unlabeled_file:
        unlabeled_reader = csv.reader(unlabeled_file)
        for index, row in enumerate(unlabeled_reader):
            unlabeled_data.append(row)

    return unlabeled_data

def translate_data(labeled_data):
    """
    Translate data from Tagalog to English.

    Args:
        labeled_data: Array that contains labeled data.

    Returns:
        translated_text_array: Array that contains translations for the text data.
    """
    
    translator = Translator()
    first_row = labeled_data[0]
    text_index = first_row.index("text")
    for index, row in enumerate(labeled_data):
        if index != 0:
            original_text = row[text_index]
            try:
                row[text_index] = translator.translate(original_text, src="tl", dest="en").text
            except:
                print(f"The following text could not be translated: {original_text}")
                row[text_index] = "Text could not be translated."
        if index % 10 == 0:
            print(f"Translation Index: {index}")
    
    return labeled_data

def write_to(abs_path, translated_data):
    """
    Writes labeled data to a specific file path.

    Args:
        abs_labeled_path: String for labeled path to data.
        labeled_data: Array that contains translated data.
    """

    with open(abs_path, 'w', newline='', encoding = "utf-8") as labeled_file:
        labeled_writer = csv.writer(labeled_file)
        for data in translated_data:
            labeled_writer.writerow(data)

if __name__ == "__main__":

    # Get Paths.
    abs_unlabeled_path, abs_translated_path = initialize_paths()

    # Get Untranslated Data.
    unlabeled_data = initialize_data(abs_unlabeled_path)

    # Translate Data. 
    translated_data = translate_data(unlabeled_data)

    # Write to Translated File Path.
    write_to(abs_translated_path, translated_data)