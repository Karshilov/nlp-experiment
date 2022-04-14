from transformers import BertTokenizer

pretrained = "./pretrained"
tokenizer = BertTokenizer.from_pretrained(pretrained)

max_length = 1024

#%%
data_path = './train.txt'
eval_path = './eval.txt'
data = []
from datasets import load_dataset
train_dataset = load_dataset('text', data_files=data_path)
eval_dataset = load_dataset('text', data_files=eval_path)

#%%
def preprocess(batch): 
    tokenized = tokenizer(
        batch["text"], 
        max_length=max_length,
        truncation=True,
        padding="max_length",
        )
    return dict(input_ids=tokenized.input_ids, labels=tokenized.input_ids)

train_dataset \
    .map(preprocess, batched=True, num_proc=7, remove_columns=["text"]) \
    .save_to_disk(f"./processed/gpt2_train")
eval_dataset \
    .map(preprocess, batched=True, num_proc=7, remove_columns=["text"]) \
    .save_to_disk(f"./processed/gpt2_eval")