from datasets import load_dataset
from transformers import AutoTokenizer
from transformers import DataCollatorWithPadding
from transformers import AutoModelForSequenceClassification, TrainingArguments, Trainer
import numpy as np
from huggingface_hub import login
from sklearn.model_selection import train_test_split
import evaluate
from datasets import DatasetDict
from Modify_Dataset import *
import torch

#!Saving for later, not enough vram to fine tune this model :(


print(torch.cuda.is_available())

# Returns a token pretty much
def preprocess_function(examples):
    return tokenizer(examples["text"], truncation=True, padding="max_length")

# Helps turn logits into useful statistical functions using np.argmax,
# and also computes the accuracy by using the compute method which looks at the validation key
def compute_metrics(eval_pred):
    predictions, labels = eval_pred

    # Turns logits into useful statistics
    predictions = np.argmax(predictions, axis=1)
    return accuracy.compute(predictions=predictions, references=labels)



# Load the dataset
dataset = createDataset("Datasets\Geared_Responsed.json")




dataset=split(dataset)




labels = dataset["train"].features["label"].names


label2id = {label: idx for idx, label in enumerate(labels)}
id2label = {idx: label for idx, label in enumerate(labels)}
num_labels = len(labels)

tokenizer = AutoTokenizer.from_pretrained("gpt2")
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
accuracy = evaluate.load("accuracy")


tokenizer.pad_token = tokenizer.eos_token
tokenizer.cls_token = tokenizer.eos_token
tokenizer.mask_token = tokenizer.eos_token
tokenizer.sep_token = tokenizer.eos_token


tokenizer.padding_side = "right"  # Ensure padding is added to the right side of the sequence


tokenized_dataset = dataset.map(preprocess_function, batched=True)

model = AutoModelForSequenceClassification.from_pretrained(
    "gpt2", num_labels=num_labels, id2label=id2label, label2id=label2id
)


device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)



data_collator = DataCollatorWithPadding(tokenizer=tokenizer)




training_args = TrainingArguments(
    output_dir = "C:\\Users\\eggsc\Documents\\A.I learning\\Fine_Tuned_GPT2",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    logging_strategy="epoch",
    gradient_accumulation_steps=2,
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    weight_decay=0.01,
    num_train_epochs=10,
    load_best_model_at_end=True,
    metric_for_best_model="eval_loss",
    greater_is_better=False,
    fp16=False,
    push_to_hub=False,
    
   

)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["eval"],  # Use test_dataset for evaluation
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics

    
)

trainer.train()

#trainer.push_to_hub()

