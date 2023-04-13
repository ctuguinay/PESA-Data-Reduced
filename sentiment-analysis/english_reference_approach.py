import torch
if torch.cuda.is_available():
  torch.cuda.empty_cache()
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from transformers import DataCollatorWithPadding, pipeline
import numpy as np
import pandas as pd
from datasets import load_dataset
import gc
import evaluate
import wandb
import os
import scipy
import sklearn

def initialize_data():
    data = load_dataset('csv', data_files = os.path.join("data",
        "labeled", "cleaned", "combined", "data_relevance_training.csv"), encoding='utf8')

    return data


def relevance_to_label(relevance):
    if relevance == "relevant":
        return 1
    elif relevance == "irrelevant":
        return 0
    else:
        raise ValueError(f"Invalid Relevance Value: {relevance}")

def compute_metrics(eval_preds):
    metric = evaluate.load("glue", "mrpc")
    logits, labels = eval_preds
    predictions = np.argmax(logits, axis=-1)
    return metric.compute(predictions=predictions, references=labels)

def encode(training_data):

    return tokenizer(training_data['text'], truncation=True, padding='max_length')

if __name__ == "__main__":

    data = initialize_data()

    data = data.map(lambda x: {"labels": relevance_to_label(x['relevance'])})

    tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

    data = data.map(encode, batched=True)

    data.set_format(type='torch', columns=['input_ids', 'attention_mask', 'labels'])
    data = data.remove_columns(['relevance', 'type', 'post_id', 'refer_post_id', 'source', 'text', 'date'])
    datasets = data['train'].train_test_split(test_size = 0.2, train_size = 0.8, seed = 0)
    training_data = datasets['train']
    validation_data = datasets['test']

    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    gc.collect()

    model = AutoModelForSequenceClassification.from_pretrained('distilbert-base-uncased')
    if torch.cuda.is_available():
        device = torch.device('cuda')
        model.cuda()
    else:
        device = torch.device('cpu')

    
    training_args = TrainingArguments("ADD EXPERIMENT NAME HERE",
                                  logging_steps=50,
                                  optim="adamw_torch",
                                  evaluation_strategy="epoch",
                                  save_strategy="epoch",
                                  report_to="wandb",
                                  load_best_model_at_end=True)

    trainer = Trainer(
        model,
        training_args,
        train_dataset=training_data,
        eval_dataset=validation_data,
        data_collator=data_collator,
        tokenizer=tokenizer,
        compute_metrics=compute_metrics,
    )

    trainer.train()

    wandb.finish()

    # LOAD MODEL

    # Initialize Wandb Run
    run = wandb.init()
    model_artifact = run.use_artifact("INSERT ARTIFACT LINK HERE", type='model')

    # Download model weights to a folder and return the path
    model_dir = model_artifact.download()

    # Load your Hugging Face model from that folder
    #  using the same model class
    loaded_model = AutoModelForSequenceClassification.from_pretrained(model_dir)

    loaded_tokenizer = AutoTokenizer.from_pretrained(model_dir)


    text_classifier = pipeline(task="text-classification", model=loaded_model, tokenizer=loaded_tokenizer)

    classification = text_classifier("Imagine if late president ferdinand marcos sr was still alive and witnessed this glorious moment sneezing . that's the president of the mass sweet and cute dad solid bbm smiling with hearts smiling with hearts smiling with hearts")

    print(classification)

    classification = text_classifier("Long live APO UN PBBM Red Heart Red Heart The AFTR shocks are still on the ABRA POEPICENTER STAYSAFE FOLDED HANDS FOLDED HANDS Bangonabrenios . Red Heart")

    print(classification)

    classification = text_classifier("The amount of appreciation gratitude and respect he has for the frontliners . Don't Irene Marcos unn seconds turned shade")

    print(classification)

    classification = text_classifier("random word")

    print(classification)