from datasets import load_dataset, Dataset
from huggingface_hub import login
from sklearn.model_selection import train_test_split
import random
from datasets import Dataset, DatasetDict, ClassLabel, Features, Value
from datasets import Dataset
import json
from datasets import Dataset, concatenate_datasets




def split(dataset):
    # Shuffle the indices of the data randomly
    num_rows = len(dataset["train"])
    shuffled_indices = list(range(num_rows))
    random.shuffle(shuffled_indices)

    # Calculate the index to split the data in half
    split_index = num_rows // 2

    # Create two new Datasets by selecting shuffled indices
    split1_dataset = dataset["train"].select(shuffled_indices[:split_index])
    split2_dataset = dataset["train"].select(shuffled_indices[split_index:])

    # Create a new DatasetDict with the two splits
    split_dataset_dict = DatasetDict({
        "train": split1_dataset,
        "eval": split2_dataset
    })


    return split_dataset_dict


def append_Data(Dataset, New_data):
       
       #The New_data is expected to be a dictionary that we will then convert to a dataset
        New_DataSet= Dataset.from_dict(New_data)
    
        return Dataset.concat(New_DataSet)

       


def createDataset(directory):
    # Load the JSON content into a Python object
    with open(directory, 'r') as file:
        data = json.load(file)

    # Initialize empty lists to store text and label data
    texts = []
    labels = []

    # Iterate over the data dictionary and extract text and label
    for label, text_list in data.items():
        texts.extend(text_list)
        labels.extend([label] * len(text_list))

    # Define the features for the dataset
    features = Features({
        "text": Value(dtype='string', id=None),
        "label": ClassLabel(names=list(data.keys()), id=None)
    })

    # Create a new Dataset object with the extracted data and features
    new_dataset = Dataset.from_dict({"text": texts, "label": labels}, features=features)

    return  DatasetDict({"train": new_dataset})



def concatenate_datasets_with_mapping(dataset1, dataset2, label_mapping1, label_mapping2):
    # Make a copy of the datasets to avoid modifying the original datasets
    dataset1 = dataset1.copy()
    dataset2 = dataset2.copy()

    # Rename the labels in dataset1 based on the provided label_mapping1
    dataset1 = dataset1.rename_column("label", "old_label1")
    dataset1 = dataset1.map(lambda example: {"label": label_mapping1[example["old_label1"]]})

    # Rename the labels in dataset2 based on the provided label_mapping2
    dataset2 = dataset2.rename_column("label", "old_label2")
    dataset2 = dataset2.map(lambda example: {"label": label_mapping2[example["old_label2"]]})

    # Concatenate the two datasets
    combined_dataset = concatenate_datasets([dataset1, dataset2])

    return combined_dataset




def dataset_to_dict(dataset):


    data_dict = dataset.data
    data_dict["label"] = dataset["train"].feature.decode_batch(data_dict["label"])
    return data_dict    

dataset = load_dataset("snips_built_in_intents")
print(dataset)



#train_dataset_dict = dataset_to_dict(dataset["train"])


print(    dataset.data
)

