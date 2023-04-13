from googletrans import Translator
import random
import csv
import os

def get_text():
    """
    Grab data from labeled data.

    Returns:
        random_text: String that contains random value for classification purposes.
    """

    rel_data_path = "data/unlabeled/cleaned/combined/data.csv"
    script_dir = os.path.dirname(__file__)
    abs_labeled_path = os.path.join(script_dir, rel_data_path).replace("sentiment-analysis\\", "")

    labeled_data = []
    while True:
        with open(abs_labeled_path, 'r', encoding = "utf-8") as unlabeled_file:
            unlabeled_reader = csv.reader(unlabeled_file)
            reader_length = 35379
            random_index = random.randint(1, reader_length - 1)
            for index, row in enumerate(unlabeled_reader):
                if index == random_index:
                    text = get_reference_post(row[1], row[4])
                    if text:
                        return translate_data(text) + " . " + translate_data(row[0])

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

if __name__ == "__main__":

    # Print Random Text for Classification
    print(get_text())