#%%
from transformers import BertTokenizer, GPT2LMHeadModel, TextGenerationPipeline
tokenizer = BertTokenizer.from_pretrained("./gpt2_model")
model = GPT2LMHeadModel.from_pretrained("./gpt2_model")
text_generator = TextGenerationPipeline(model, tokenizer)   
prefix = "我"
prefix = text_generator(prefix, max_new_tokens=100, do_sample=True)[0]["generated_text"]
print(prefix)
# %%
