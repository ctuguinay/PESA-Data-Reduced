from googletrans import Translator
import csv
import os

def initialize_data():
    """
    Grab data from unlabeled data.

    Returns:
        labeled_data: Array that contains labeled data.
    """

    rel_data_path = "data/unlabeled/cleaned/combined/data.csv"
    script_dir = os.path.dirname(__file__)
    abs_cleaned_path = os.path.join(script_dir, rel_data_path).replace("sentiment-analysis\\", "")
    data = []
    with open(abs_cleaned_path, 'r', encoding = "utf-8") as unlabeled_file:
        unlabeled_reader = csv.reader(unlabeled_file)
        for index, row in enumerate(unlabeled_reader):
            if index != 0:
                text = get_reference_post(row[1], row[4])
                if text:
                    row[0] = translate_data(text) + " . " + translate_data(row[0])
            data.append(row)
            if index % 10 == 0:
                print(f"Index: {index}")
            if index >= 1000:
                break

    return data

def get_reference_post(media_source, refer_post_id):
    """
    Gets the text for which a post is referring to.

    Args:
        media_source: String that contains the media source.
        refer_post_id: String that contains the id for the original post.

    Returns:
        text: String that represents the text from the original post or a None type object.
    """

    rel_data_path = "data/unlabeled/cleaned/combined/data.csv"
    script_dir = os.path.dirname(__file__)
    abs_cleaned_path = os.path.join(script_dir, rel_data_path).replace("sentiment-analysis\\", "")


    with open(abs_cleaned_path, 'r', encoding = "utf-8") as labeled_file:
        labeled_reader = csv.reader(labeled_file)
        for index, row in enumerate(labeled_reader):
            if index != 0:
                if row[1] == media_source and row[4] == refer_post_id:
                    return row[0]

    return None

def translate_data(text):
    """
    Translate data from Tagalog to English.

    Args:
        text: String that has not been translated.

    Returns:
        text: String that has been translated.
    """

    translator = Translator()
    try:
        text = translator.translate(text, src="tl", dest="en").text
    except:
        print(f"The following text could not be translated: {text}")
    
    return text

def write_to(labeled_data):
    """
    Writes labeled data to a specific training file path.

    Args:
        labeled_data: Array of rows of labeled data.
    """

    rel_data_path = "data/unlabeled/cleaned/combined/data_pre_filtering.csv"
    script_dir = os.path.dirname(__file__)
    abs_cleaned_path = os.path.join(script_dir, rel_data_path).replace("sentiment-analysis\\", "")

    with open(abs_cleaned_path, 'w', newline='', encoding = "utf-8") as labeled_file:
        labeled_writer = csv.writer(labeled_file)
        for data in labeled_data:
            labeled_writer.writerow(data)

if __name__ == "__main__":

    # Get Referenced and Translated Data.
    data = initialize_data()

    # Write Labeled Data to a Training File.
    write_to(data)