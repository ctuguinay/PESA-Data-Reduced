# Sentiment Analysis Subdirectory

Make sure you are in the current directory with the following command: 
```
cd sentiment-analysis
```

## Quickstart

Run the following to create the training data:
```
python create_training.py
```

Upload English_Reference_Approach.ipynb into Google Colab to train and test the relevancy sequence classifier model.

Place `data\labeled\cleaned\combined\data_relevance_training.csv` within the Google Colab files.

Run the code, follow the prompts to login to wandb, and place the correct artifact link to grab the necessary model and tokenizer version.

Run the following to get a sentence that matches the data within `data\labeled\cleaned\combined\data_relevance_training.csv` for further test classification:
```
python get_text_for_classification.py
```