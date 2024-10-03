# Polarisation analysis through contextual embeddings

**Paper:** _On the difficulty of using Contextual Word Embeddings to Measure Political Polarisation in Parliamentary Speech_ ([pdf](paper.pdf))  
**Author:** Giulio Cusenza ([email](mailto:giuliocusenza@gmail.com))  
**Supervisor:** Çağrı Çöltekin  

## Info
This repository contains the code framework used in the afore-mentioned study to measure political polarisation in parliamentary debates from the United Kingdom and Italy.

The folder [Code/](./Code/) contains the scripts used the experiment. The main pipeline is constituted by:
1. [extract_text.py](./Code/extract_text.py)
2. [embed.py](./Code/embed.py)
3. [semantic_polarity.py](./Code/semantic_polarity.py)

The folder [Code/data/](./Code/data/) contains:
- ParlaMint 4.1's datasets for the UK's House of Commons and the Italian Senate.
- extracted utterances including selected topical words from major parties.
- BERT-derived contextual embeddings of these topical words.
- semantic polarity matrices defined in the study.
