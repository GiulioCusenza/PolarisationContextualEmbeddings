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

The experiment is based on data from [ParlaMint 4.1](https://www.clarin.eu/parlamint). These data are to be downloaded separately for each country and stored in the appropriate folder ([GB/ParlaMint/](./Code/data/GB/) or [IT/ParlaMint/](./Code/data/IT/)). Simply download the datasets and move the content from the "TEI" directories into the afore-mentioned folders.

The folder [Code/data/](./Code/data/) also contains the intermediate outputs of the experiments, namely:
- extracted utterances including selected topical words from major parties.
- BERT-derived contextual embeddings of these topical words.
- semantic polarity matrices described in the study.
