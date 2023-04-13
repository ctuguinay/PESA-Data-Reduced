import os
import sys
import csv
import argparse

def argparse_create(args):
    """
    Parser to parse this script's arguments that pertain to our labeling tool.

    Args:
        args: User inputted arguments that have yet to be parsed.

    Returns:
        parsed_args: Parsed user inputted arguments.
    """

    parser = argparse.ArgumentParser(description='Argument parser for creating the genereated dataset CSVs.')

    parser.add_argument("--media_source", type=str,
            help="Media source we want to label. Use: \"combined\", \"source_one\", \"source_two\", \"source_three\", \"source_four\", or \"source_five\".",
            default="source_five")

    parser.add_argument("--make_new_labeled", type=str,
        help="Whether we want to make a new labeled dataset. Use: \"True\" or \"False\".",
        default="False")

    parser.add_argument("--use_translator", type=str,
        help="Whether we want view the translations of text. Use: \"True\" or \"False\".",
        default="True")

    parser.add_argument("--labeling_category", type=str,
        help="Whether we want view the cleaned versions of text. Use: \"Relevance\" or \"Sentiment\".",
        default="Sentiment")

    # Parse arguments.
    parsed_args = parser.parse_args(args)

    return parsed_args

def initialize_paths(clean_status, media_source, labeling_category):
    """
    Initialize relevant paths to to-be translated data and translated data.

    Args:
        clean_status: String that describes location and cleaned status of data.
        media_source: String that describes media source of data.
        labeling_category: String that describes what we will be labeling.

    Returns:
        abs_unlabeled_path: String for unlabeled path to data.
        abs_labeled_path: String for labeled path to data.
    """

    # Get relevant paths.
    rel_data_path = "data/unlabeled/" + clean_status + "/" + media_source + "/" + "data_sample.csv"
    script_dir = os.path.dirname(__file__)
    abs_unlabeled_path = os.path.join(script_dir, rel_data_path).replace("labeling\\", "")

    # Check that abs_unlabeled_path exists.
    if not os.path.exists(abs_unlabeled_path):
        raise ValueError(f"There exists no data.csv within {abs_unlabeled_path}.")

    # Get target labeled path location.
    labeling_category = labeling_category.lower()
    abs_labeled_path = os.path.join(script_dir, rel_data_path).replace("labeling\\", "").replace("unlabeled", "labeled")
    abs_labeled_path = abs_labeled_path.replace("data_sample.csv", "data_sample_" + labeling_category + ".csv")

    return abs_unlabeled_path, abs_labeled_path

def initialize_labeled_data(abs_unlabeled_path, abs_labeled_path, make_new_labeled):
    """
    Check if labeled data csv already exists and grab data from it and if it does not exist, 
    we grab data from just the unlabeled data.

    Args:
        abs_unlabeled_path: String for unlabeled path to data.
        abs_labeled_path: String for labeled path to data.
        make_new_labeled: Boolean to make new labeled dataset or to use existing data.

    Returns:
        labeled_data: Array that contains labeled data.
    """
    labeled_data = []
    if os.path.exists(abs_labeled_path) and not make_new_labeled:
        with open(abs_labeled_path, 'r', encoding = "utf-8") as labeled_file:
            labeled_reader = csv.reader(labeled_file)
            for row in labeled_reader:
                labeled_data.append(row)
    else:
        with open(abs_unlabeled_path, 'r', encoding = "utf-8") as unlabeled_file:
            unlabeled_reader = csv.reader(unlabeled_file)
            for index, row in enumerate(unlabeled_reader):
                if index == 0:
                    if "relevance" in abs_labeled_path:
                        row.append("relevance")
                    elif "sentiment" in abs_labeled_path:
                        row.append("sentiment")
                else:
                    row.append("")
                labeled_data.append(row)

    return labeled_data

def initialize_translated_data():
    """
    Initialize translated data.

    Returns:
        translated_text_array: Array that contains translations for the text data.
    """

    # Get relevant paths.
    rel_data_path = "data/unlabeled/cleaned/source_five/data_sample_translated.csv"
    script_dir = os.path.dirname(__file__)
    abs_translated_path = os.path.join(script_dir, rel_data_path).replace("labeling\\", "")

    # Check that abs_unlabeled_path exists.
    if not os.path.exists(abs_translated_path):
        raise ValueError(f"There exists no data_sample_translated.csv within {abs_translated_path}.")

    translated_text_array = []
    with open(abs_translated_path, 'r', encoding = "utf-8") as translated_file:
        translated_reader = csv.reader(translated_file)
        for index, row in enumerate(translated_reader):
            translated_text_array.append(row)

    return translated_text_array

def labeling_relevance(uncleaned_labeled_data, cleaned_labeled_data, use_translator, *translated_text_array):
    """
    Label data with relevance values.

    Args:
        uncleaned_labeled_data: Array that contains uncleaned unlabeled or labeled data that will be modified.
        cleaned_labeled_data: Array that contains cleaned unlabeled or labeled data that will be modified.
        use_translator: Boolean that decides if the program will make use of a translator.
        translated_text_array: Array that contains strings for the translations of the cleaned text data.

    Returns:
        uncleaned_labeled_data: Array that contains uncleaned unlabeled or labeled data that has been modified.
        cleaned_labeled_data: Array that contains cleaned unlabeled or labeled data that has been modified.
    """

    still_labeling = True
    labeled_data_length = len(cleaned_labeled_data)
    labeled_data_row_length = len(cleaned_labeled_data[0])
    index = 1
    print("Type a command and press enter. For more help, type the command \"h\".")

    try:
        while still_labeling:
            print("-"*30)
            print(f"Labeled Data Index: {index}")
            print(f"Relevance: {uncleaned_labeled_data[index][6]}")
            #try:
            #    print(f"Reference Text: {get_reference_post(uncleaned_labeled_data[index][1], uncleaned_labeled_data[index][4])}")
            #except:
            #    print("Reference Text: N/A")
            print(f"Uncleaned Text: {uncleaned_labeled_data[index][0]}")
            print(f"Cleaned Text: {cleaned_labeled_data[index][0]}")
            if use_translator:
                print(f"Cleaned Translated Text: {translated_text_array[0][index][0]}")
            user_input = input("Command: ")
            if user_input == "+":
                uncleaned_labeled_data[index][labeled_data_row_length - 1] = "relevant"
                cleaned_labeled_data[index][labeled_data_row_length - 1] = "relevant"
                if index == labeled_data_length - 1:
                    index = 1
                else:
                    index = index + 1
            elif user_input == "-":
                uncleaned_labeled_data[index][labeled_data_row_length - 1] = "irrelevant"
                cleaned_labeled_data[index][labeled_data_row_length - 1] = "irrelevant"
                if index == labeled_data_length - 1:
                    index = 1
                else:
                    index = index + 1
            elif user_input == "a":
                if index == 1:
                    index = labeled_data_length - 1
                else:
                    index = index - 1
            elif user_input == "d":
                if index == labeled_data_length - 1:
                    index = 1
                else:
                    index = index + 1
            elif user_input == "i":
                index_user_input = input("Index: ")
                if index_user_input.isnumeric():
                    index_user_input = int(index_user_input)
                    if index_user_input > 0 and index_user_input < labeled_data_length:
                        index = index_user_input
                    else:
                        print(f"Index {index_user_input} does not exist.")
                else:
                    print("Index Values is not of type int.")
            elif user_input =="q":
                still_labeling = False
            elif user_input == "h":
                print("Commands:")
                print("+ is to add a relevant label to the labeled data.")
                print("- is to add an irrelevant label to the labeled data.")
                print("a is to move back an index.")
                print("d is to move forward an index.")
                print("i is to set a specific index.")
                print("q is to quit labeling.")
                print("h is to get help for commands.")
            else:
                print("Invalid Argument. Enter h to get help for commands.")

            print("-"*30)
            print("")
        
        return uncleaned_labeled_data, cleaned_labeled_data
        
    except:

        return uncleaned_labeled_data, cleaned_labeled_data

def labeling_sentiment(uncleaned_labeled_data, cleaned_labeled_data, use_translator, *translated_text_array):
    """
    Label data with sentiment values.

    Args:
        uncleaned_labeled_data: Array that contains uncleaned unlabeled or labeled data that will be modified.
        cleaned_labeled_data: Array that contains cleaned unlabeled or labeled data that will be modified.
        use_translator: Boolean that decides if the program will make use of a translator.
        translated_text_array: Array that contains strings for the translations of the cleaned text data.

    Returns:
        uncleaned_labeled_data: Array that contains uncleaned unlabeled or labeled data that has been modified.
        cleaned_labeled_data: Array that contains cleaned unlabeled or labeled data that has been modified.
    """

    still_labeling = True
    labeled_data_length = len(cleaned_labeled_data)
    labeled_data_row_length = len(cleaned_labeled_data[0])
    index = 1
    print("Type a command and press enter. For more help, type the command \"h\".")

    try:
        while still_labeling:
            print("-"*30)
            print(f"Labeled Data Index: {index}")
            print(f"Sentiment: {cleaned_labeled_data[index][6]}")
            #try:
            #    print(f"Reference Text: {get_reference_post(uncleaned_labeled_data[index][1], uncleaned_labeled_data[index][4])}")
            #except:
            #    print("Reference Text: N/A")
            print(f"Uncleaned Text: {uncleaned_labeled_data[index][0]}")
            print(f"Cleaned Text: {cleaned_labeled_data[index][0]}")
            if use_translator:
                print(f"Cleaned Translated Text: {translated_text_array[0][index][0]}")
            user_input = input("Command: ")
            if user_input == "+":
                uncleaned_labeled_data[index][labeled_data_row_length - 1] = "positive"
                cleaned_labeled_data[index][labeled_data_row_length - 1] = "positive"
                if index == labeled_data_length - 1:
                    index = 1
                else:
                    index = index + 1
            elif user_input == "=":
                uncleaned_labeled_data[index][labeled_data_row_length - 1] = "neutral"
                cleaned_labeled_data[index][labeled_data_row_length - 1] = "neutral"
                if index == labeled_data_length - 1:
                    index = 1
                else:
                    index = index + 1
            elif user_input == "-":
                uncleaned_labeled_data[index][labeled_data_row_length - 1] = "negative"
                cleaned_labeled_data[index][labeled_data_row_length - 1] = "negative"
                if index == labeled_data_length - 1:
                    index = 1
                else:
                    index = index + 1
            elif user_input == "a":
                if index == 1:
                    index = labeled_data_length - 1
                else:
                    index = index - 1
            elif user_input == "d":
                if index == labeled_data_length - 1:
                    index = 1
                else:
                    index = index + 1
            elif user_input == "i":
                index_user_input = input("Index: ")
                if index_user_input.isnumeric():
                    index_user_input = int(index_user_input)
                    if index_user_input > 0 and index_user_input < labeled_data_length:
                        index = index_user_input
                    else:
                        print(f"Index {index_user_input} does not exist.")
                else:
                    print("Index Values is not of type int.")
            elif user_input =="q":
                still_labeling = False
            elif user_input == "h":
                print("Commands:")
                print("+ is to add a positive sentiment to the labeled data.")
                print("= is to add a neutral sentiment to the labeled data.")
                print("- is to add a negative sentiment to the labeled data.")
                print("a is to move back an index.")
                print("d is to move forward an index.")
                print("i is to set a specific index.")
                print("q is to quit labeling.")
                print("h is to get help for commands.")
            else:
                print("Invalid Argument. Enter h to get help for commands.")

            print("-"*30)
            print("")
    
        return uncleaned_labeled_data, cleaned_labeled_data
    
    except:

        return uncleaned_labeled_data, cleaned_labeled_data

def get_reference_post(media_source, refer_post_id):
    """
    Gets the text for which a post is referring to.

    Args:
        media_source: String that contains the media source.
        refer_post_id: String that contains the id for the original post.

    Returns:
        text: String that represents the text from the original post or a message saying post does not exist.
    """

    rel_data_path = "data/unlabeled/uncleaned/source_five/data.csv"
    script_dir = os.path.dirname(__file__)
    abs_unlabeled_path = os.path.join(script_dir, rel_data_path).replace("labeling\\", "")


    with open(abs_unlabeled_path, 'r', encoding = "utf-8") as unlabeled_file:
        unlabeled_reader = csv.reader(unlabeled_file)
        for index, row in enumerate(unlabeled_reader):
            if row[1] == media_source and row[4] == refer_post_id:
                return row[0]

    return "Reference Post Does Not Exist"

def write_to_labeled(abs_labeled_path, labeled_data):
    """
    Writes labeled data to a specific file path.

    Args:
        abs_labeled_path: String for labeled path to data.
        labeled_data: Array that contains labeled data that has been modified.
    """

    with open(abs_labeled_path, 'w', newline='', encoding = "utf-8") as labeled_file:
        labeled_writer = csv.writer(labeled_file)
        for data in labeled_data:
            labeled_writer.writerow(data)

if __name__ == "__main__":

    # Get parsed args.
    args = argparse_create((sys.argv[1:]))

    media_source = args.media_source
    pre_make_new_labeled = args.make_new_labeled
    if pre_make_new_labeled == "True":
        make_new_labeled = True
    elif pre_make_new_labeled == "False":
        make_new_labeled = False
    else:
        raise ValueError("--make_new_labeled is neither \"True\" nor \"False\".")
    pre_use_translator = args.use_translator
    if pre_use_translator == "True":
        use_translator = True
    elif pre_use_translator == "False":
        use_translator = False
    else:
        raise ValueError("--use_translator is neither \"True\" nor \"False\".")
    labeling_category = args.labeling_category
    if labeling_category != "Relevance" and labeling_category != "Sentiment":
        raise ValueError("--labeling_cateogry is neither \"Relevance\" nor \"Sentiment\".")

    # Initialize Paths.
    abs_unlabeled_uncleaned_path, abs_labeled_uncleaned_path = initialize_paths("uncleaned", media_source, labeling_category)
    abs_unlabeled_cleaned_path, abs_labeled_cleaned_path = initialize_paths("cleaned", media_source, labeling_category)
    
    # Initialize Labeled Data.
    uncleaned_labeled_data = initialize_labeled_data(abs_unlabeled_uncleaned_path, abs_labeled_uncleaned_path, make_new_labeled)
    cleaned_labeled_data = initialize_labeled_data(abs_unlabeled_cleaned_path, abs_labeled_cleaned_path, make_new_labeled)

    if use_translator:
        # Initialize Translated Text Data
        translated_cleaned_text_array = initialize_translated_data()

    # Label data.
    if labeling_category == "Relevance":
        if use_translator:
            uncleaned_labeled_data, cleaned_labeled_data = labeling_relevance(uncleaned_labeled_data, cleaned_labeled_data, use_translator, translated_cleaned_text_array)
        else:
            uncleaned_labeled_data, cleaned_labeled_data = labeling_relevance(uncleaned_labeled_data, cleaned_labeled_data, use_translator)
    else:
        if use_translator:
            uncleaned_labeled_data, cleaned_labeled_data = labeling_sentiment(uncleaned_labeled_data, cleaned_labeled_data, use_translator, translated_cleaned_text_array)
        else:
            uncleaned_labeled_data, cleaned_labeled_data = labeling_sentiment(uncleaned_labeled_data, cleaned_labeled_data, use_translator)

    # Write to target labeled files.
    write_to_labeled(abs_labeled_uncleaned_path, uncleaned_labeled_data)
    write_to_labeled(abs_labeled_cleaned_path, cleaned_labeled_data)