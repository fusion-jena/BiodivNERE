# BiodivNERE [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6575865.svg)](https://doi.org/10.5281/zenodo.6575865)
* BiodivNER+RE are two corpora that are meant to be for Named Entity Recognition (NER) and Relation Extraction (RE) tasks.
* Such corpora are designed for machine learning technique 
  * NER -> TokenClassification Models
  * RE -> SequenceClassification Models
* You can download [BiodivNER corpus](https://doi.org/10.5281/zenodo.6458503) and [BiodivRE corpus](https://doi.org/10.5281/zenodo.6458503) directly from Zenodo. 
* This repo provided our used scripts to construct and analyze such corpora.

## 1. Named Entity Recognition Scripts (NER)
This [/NER](/NER) directory contains our used script to construct our BiodivNER corpus.
BiodivNER is doubly annotated corpus. This means 2 annotator per file are assigned.
1. `ner_agreement.py` calculates Cohen's Kappa score for the double annotation of the corpus
   1. Avg. agreement score for 4 annotator/2 annotator pairs = 0.71
2. `ner_get_matches.py` it extracts the matches where the annotator pair agreed exactly on the same annotation.
3. `ner_get_mismatches.py` it extracts the mismatches where the annotator pair disagreed on the answer, the result from this script is then reconciled by each annotator pair to came up with a final annotation.
4. `train_test_split.py` creates the three folds of the train/dev/test splits with 80%, 10%, and 10% respectively.
5. `ner_statistics.py` analyzes the BiodivNER corpus as well as the state-of-the-art corpora for comparison in terms of:
   1. Class distribution
   2. \# Sentences
   3. \# Words
   4. \# Mentions (Annotations)
   5. \# Unique Mentions (Unique Annotations)

## 2. Relation Extraction Scripts (RE)
The [/RE](/RE) directory lists our scripts to create and analyze BiodivRE corpus.
BiodivRE is build ontop of the BiodivNER corpus.
1. `re_init_corpus.py` 
   1. transforms the BiodivNER data into horizontal sequences (a.k.a transpose of BiodivNER)
   2. create variations for sentences with more than 2 named entities, to ensure that a sentence has exactly 2 named entities.
   3. provides 2 sampler mechanisms to select from the created variations, we compare between them in our paper.
      1. Random sampler (tired)
      2. Round-Robin based on the supported relations by the new version of the BiodivOnto (tried+selected). 
2. `re_agreement.py` initially we doubly annotated a small set of the corpus (50 sentences), this script calculates the Cohen's Kappa score for this subset
   1. agreement score = 0.93
3. `re_anonymize_split.py` embeds the named entity tag to the actual sentence to facilitate the training tasks. In addition, it apply the train-test split as BiodivNER (see above).
   1. "**The @QUALITY$ of the @ORGANISM# is measured vertically for alive ones.**" is derived from the following:

| The   |      height      |  of | the   |      tree  | is    |  measured | vertically | for | alive | ones | .| 
|----------|:----------------:|------:|-------|:-------|:-------:|------:|------|:-----:|------:|:-----:|------:|
| O   |      QUALITY  |O| O   | ORGANISM  | O | O | O | O | O | O | O|
4. `re_statistics.py` analyzes the BiodivRE corpus, it counts the binary and multi-label relation inside the corpus.

## Citation

## Acknowledgement
* The authors thank the Carl Zeiss Foundation for the financial support of the project "A Virtual Werkstatt for Digitization in the Sciences (K3, P5)" within the scope of the program line "Breakthroughs: Exploring Intelligent Systems for Digitization -  explore the basics, use applications". 
* Alsayed Algergawy' work has been funded by the "Deutsche Forschungsgemeinschaft (DFG)" as part of CRC 1076.
