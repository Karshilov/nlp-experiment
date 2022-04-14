import os
from transformers import BertTokenizer, GPT2LMHeadModel, GPT2Config
from datasets import load_from_disk
from transformers import Seq2SeqTrainer, Seq2SeqTrainingArguments, DataCollatorForSeq2Seq

pretrained="./pretrained"
model = GPT2LMHeadModel.from_pretrained(pretrained)
tokenizer = BertTokenizer.from_pretrained(pretrained)

output_dir = f"./gpt2_model"

training_args = Seq2SeqTrainingArguments(
    output_dir=output_dir,

    learning_rate=5e-5,
    num_train_epochs=1,
    max_steps=-1,
    evaluation_strategy="steps",
    eval_steps=2000,

    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    gradient_accumulation_steps=6,
    eval_accumulation_steps=8,

    adafactor=True,
    lr_scheduler_type="linear",
    warmup_steps=2000,

    logging_steps=100,
    save_strategy="steps",
    save_steps=2000,
    save_total_limit=20,

    dataloader_num_workers=7,
)

data_collator = DataCollatorForSeq2Seq(
    tokenizer=tokenizer,
    model=model,
    padding=True,
    return_tensors="pt",
)

train_path="./processed/gpt2_train"
eval_path="./processed/gpt2_eval"

train_dataset = load_from_disk(train_path)["train"]
eval_dataset = load_from_disk(eval_path)["train"]

print(train_dataset)
print(eval_dataset)

trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    tokenizer=tokenizer,
    data_collator=data_collator,
)

train_result = trainer.train(resume_from_checkpoint=False)
metrics = train_result.metrics
trainer.log_metrics("train", metrics)
trainer.save_metrics("train", metrics)

trainer.save_model()
trainer.save_state()

eval_metrics = trainer.evaluate(num_beams=4, metric_key_prefix="eval")
trainer.log_metrics("eval", eval_metrics)
trainer.save_metrics("eval", eval_metrics)

os.system("shutdown")