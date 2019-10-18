# RasaNLUCuCo
This repository contains a collection of helpful custom components that can be used in
the Rasa NLU pipeline. 


## 1. Spellchecking

We provide a custom [Rasa](https://github.com/RasaHQ) NLU component that implements spellchecking on each token and automatically replaces misspelled tokens with the corrected version. The spellchecking itself is based on [pyspellchecker](https://github.com/barrust/pyspellchecker). The component has several parameters that can be set in the configuration file. For example, it supports multiple language ("en", "es", "de", "fr", "pt"). You can also set a distance value, which is set to 1 by default. This parameter is used in the spellchecking algorithm and for details refer to the corresponding GitHub project [pyspellchecker](https://github.com/barrust/pyspellchecker). Since the algorithm uses a word frequency list to detect misspelled words and provide the correct version, you can also provide a custom word frequency file (each row with "word, frequency" format). Note that in order to apply this custom spellchecking component in a pipeline, a tokenizer component has to be applied before in the pipeline.

Below you can find a sample configuration using the spellchecking component and providing a custom word frequency file to it.

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
