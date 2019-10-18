# RasaNLUCuCo
This repository contains a collection of helpful custom components that can be used in
the Rasa NLU pipeline. 


## 1. Spellchecking

We provide a custom Rasa component that implements spellchecking on each token and automatically replaces misspelled tokens with the corrected version. The spellchecking itself is based on [pyspellchecker](https://github.com/barrust/pyspellchecker). The component has several parameters that can be set in the configuration file. For example, it supports multiple language ("en", "es", "de", "fr", "pt"). You can also set a distance value, which is set to 1 by default. This parameter is used in the spellchecking algorithm and for details refer to the corresponding GitHub project [pyspellchecker](https://github.com/barrust/pyspellchecker).

```
pipeline:
- name: "WhitespaceTokenizer"
- name: "spellchecking.SpellCheckerCorrection"
  language: "de"
  distance: 2
  word_freq_file: "resources/de_50k.txt"
- name: "CRFEntityExtractor"
- name: "CountVectorsFeaturizer"
- name: "EmbeddingIntentClassifier"
```
