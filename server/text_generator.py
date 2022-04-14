#%%
from transformers import BertTokenizer, GPT2LMHeadModel, TextGenerationPipeline
tokenizer = BertTokenizer.from_pretrained("./gpt2_model")
model = GPT2LMHeadModel.from_pretrained("./gpt2_model")
text_generator = TextGenerationPipeline(model, tokenizer) 
yq_tokenizer = BertTokenizer.from_pretrained("./gpt2_yq_model")
yq_model = GPT2LMHeadModel.from_pretrained("./gpt2_yq_model")
yq_text_generator = TextGenerationPipeline(yq_model, yq_tokenizer)
# %%
def get_generated_text(prefix: str, model_type: bool):
    if model_type: 
        return yq_text_generator(prefix, max_new_tokens=100, do_sample=True)[0]["generated_text"]
    else:
        return text_generator(prefix, max_new_tokens=100, do_sample=True)[0]["generated_text"]