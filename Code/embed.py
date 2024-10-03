from settings import *

import torch
from collections import OrderedDict
import os, csv
from tqdm import tqdm
from beepy import beep

from transformers import AutoModelForMaskedLM, AutoTokenizer
model = AutoModelForMaskedLM.from_pretrained(MODEL,
                                             output_hidden_states = True)
tokenizer = AutoTokenizer.from_pretrained(MODEL)


def bert_text_preparation(text, tokenizer):
    """
    Preprocesses text input in a way that BERT can interpret.
    return tokenized_text, tokens_tensor, segments_tensor
    """
    inputs = tokenizer(
        text, 
        max_length=512,  # Specify the maximum token length for the model
        truncation=True,  # Enable truncation to avoid exceeding the context window
        return_tensors='pt'  # Return PyTorch tensors (optional, depends on your use case)
    )
    tokenized_text = tokenizer.convert_ids_to_tokens(inputs['input_ids'].squeeze())
    return tokenized_text, inputs["input_ids"], inputs["token_type_ids"], inputs["attention_mask"]

def get_sentence_embeddings(tokens_tensor, segments_tensor, model):
    """
    Obtains BERT embeddings for tokens.
    """
    # gradient calculation id disabled
    with torch.no_grad():
        # obtain hidden states
        outputs = model(tokens_tensor, segments_tensor)
        hidden_states = outputs["hidden_states"]
    # concatenate the tensors for all layers
    # use "stack" to create new dimension in tensor
    token_embeddings = torch.stack(hidden_states, dim=0)
    # remove dimension 1, the "batches"
    token_embeddings = torch.squeeze(token_embeddings, dim=1)
    # swap dimensions 0 and 1 so we can loop over tokens
    token_embeddings = token_embeddings.permute(1,0,2)
    # intialized list to store embeddings
    token_vecs_sum = []
    # "token_embeddings" is a [Y x 12 x 768] tensor
    # where Y is the number of tokens in the sentence
    # loop over tokens in sentence
    for token in token_embeddings:
        # "token" is a [12 x 768] tensor
        # sum the vectors from the last four layers
        sum_vec = torch.sum(token[-4:], dim=0)
        token_vecs_sum.append(sum_vec)
    return token_vecs_sum

def get_embeddings(sentences):
    """
    Get embeddings for multiple sentences.
    """
    context_embeddings = []
    context_tokens = []
    groups = []
    for group, sentence in tqdm(sentences):
        tokenized_text, input_ids, _, attention_mask = bert_text_preparation(sentence, tokenizer)
        list_token_embeddings = get_sentence_embeddings(input_ids, attention_mask, model)
        # make ordered dictionary to keep track of the position of each   word
        tokens = OrderedDict()
        # loop over tokens in sensitive sentence
        for token in tokenized_text[1:-1]:
            # keep track of position of word and whether it occurs multiple times
            if token in tokens:
                tokens[token] += 1
            else:
                tokens[token] = 1
            # compute the position of the current token
            token_indices = [i for i, t in enumerate(tokenized_text) if t == token]
            current_index = token_indices[tokens[token]-1]
            # get the corresponding embedding
            token_vec = list_token_embeddings[current_index]
            # save values
            context_embeddings.append(token_vec)
            context_tokens.append(token)
            groups.append(group)
    return context_embeddings, context_tokens, groups


if __name__ == "__main__":
    for year in YEARS:
        for topic in TOPICS:
            print(year, topic)
            in_file = UTTERANCES_DIR+year+"/"+topic+".tsv"
            out_dir = EMBEDDINGS_DIR+year+"/"+topic+"/"
            os.makedirs(out_dir, exist_ok=True)
            with open(in_file, "r", encoding="utf-8") as data:
                # get embeddings
                sentences = list()
                for _, group, _, text in csv.reader(data, delimiter="\t"):
                    sentences.append((group, text))
                embeddings, tokens, groups = get_embeddings(sentences)
                # save
                out_embeddings = csv.writer(
                        open(out_dir+"embeddings.txt", 'w', encoding="utf-8"),
                        delimiter='\t',
                        lineterminator="\n"
                    )
                out_groups = open(out_dir+"groups.txt", 'w', encoding="utf-8")
                for i, token in enumerate(tokens):
                    if token.lower() == topic.lower():
                        out_embeddings.writerow(embeddings[i].numpy())
                        out_groups.write(groups[i]+"\n")
                out_groups.close()
    beep()