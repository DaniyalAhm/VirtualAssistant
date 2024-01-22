from datasets import load_dataset,DatasetDict
from transformers import AutoTokenizer
from transformers import DataCollatorWithPadding
from transformers import AutoModelForSequenceClassification, TrainingArguments, Trainer
import numpy as np
from huggingface_hub import login
from sklearn.model_selection import train_test_split
import evaluate
import random
from datasets import DatasetDict
from transformers import TextClassificationPipeline
from Modify_Dataset import *

#login()

# Returns a token pretty much
def preprocess_function(examples):
    return tokenizer(examples["text"], truncation=True)

# Helps turn logits into useful statistical functions using np.argmax,
# and also computes the accuracy by using the compute method which looks at the validation key
def compute_metrics(eval_pred):
    predictions, labels = eval_pred

    # Turns logits into useful statistics``
    predictions = np.argmax(predictions, axis=1)
    return accuracy.compute(predictions=predictions, references=labels)



# Load the dataset
dataset = createDataset("/Geared_Responsed_no_identity copy.json")




dataset=split(dataset)




labels = dataset["train"].features["label"].names


label2id = {label: idx for idx, label in enumerate(labels)}
id2label = {idx: label for idx, label in enumerate(labels)}
num_labels = len(labels)

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
accuracy = evaluate.load("accuracy")

tokenized_dataset = dataset.map(preprocess_function, batched=True)

model = AutoModelForSequenceClassification.from_pretrained(
    "bert-base-uncased", num_labels=num_labels, id2label=id2label, label2id=label2id
)








training_args = TrainingArguments(
    #Replace with your own Output Directory
    output_dir = "/home/daniyal-ahmed/Documents/VirtualAssistant/A.I learning V.58/Fine_Tuned_BERT18",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    logging_strategy="epoch",
    gradient_accumulation_steps=2,
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    weight_decay=0.0777,
    num_train_epochs=5  ,
    load_best_model_at_end=True,
    metric_for_best_model="eval_loss",
    greater_is_better=False,
    fp16=False,
    push_to_hub=False

)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["eval"],  # Use test_dataset for evaluation
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
    
)

trainer.train()

#trainer.push_to_hub()
 
