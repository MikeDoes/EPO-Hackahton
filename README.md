# EPO Codefest and Patent Variable Team

Our team composed of Adam Novak, Michael Mazourik, Iaroslav Petrov and Konstantinos Samaras-Tsakiris aims to help solve the challenge of the European Patent Office's Codefest challenge on green plastics:

“To develop creative and reliable artificial intelligence (AI) models for automating the identification of patents related to green plastics”


## Interactive Universal Patent Classifier

The Universal Patent Classifier (UPC 2.0) allows classifications of any patent claims given a CPC classification definition

* Model extracts facts from the definition and the patent document. Then evaluates whether the patent belongs with a clear graph and text explanation

This model is available via index.html

## Notebooks

- ops_api_downloader_and_parser.ipynb -> enables the download of claims via the OPS system
- chemical_information_extraction.ipynb -> training of model which extracts facts in the form of triplets
- supervised_model_evaluations.ipynb -> benchmark for our supervised open sourced dataset
- data_augmentation.ipynb -> Data augmentation technic (DARE) using GPT-3 to create a new text to text open information exctration dataset
- fine_tunning_gpt35.ipynb -> Fine-tuning of one of the largest language model to help us with classification and information extraction used in the interactive universal patent classifier
- unsupervised_embeddings.ipynb -> Clustering of embeddings from the claims by classes
- ada_embeddings_script.ipynb -> Generation of embeddings via openai's Ada model

## Usage of Datamodule

1. Downlaod two dataset `json`s: one for the target class, and one for the other classes
2. Determine their locations on the hard drive
3. Instantiate `SupervisedDataModule` object with the following parameters:

- fname_cls -- The filepath to the class dataset json (e.g. `ds_WO_Y02W_complete_final_new.json`)
- fname_not -- The filepath to the json, which contains the data, opposite to the class from `fname_cls`
- tokenizer -- (Optional) The tokenizer object from `transformers` python module
- batch_size -- (Optional) The batch size

4. Invoke `SupervisedDataModule::prepare_data` method, and wait until tokenization process completes
5. From now on, it is possible to call: `SupervisedDataModule::train_dataloader`, `SupervisedDataModule::val_dataloader`, `SupervisedDataModule::test_dataloader` to acquire train, validation, and test `DataLoader`s (`pytorch` library).

## Usage of file paths and API Keys

- Change paths to downloaded datasets from https://doi.org/10.7910/DVN/TTP7AO
- OpenAI key can be found in presentation attached to the e-mail. NEVER push it to Github.
- OPS API Keys can be requested by the EPO at https://www.epo.org/searching-for-patents/data/web-services/ops.html
