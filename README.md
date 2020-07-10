[Multilingual Transformer Ensembles for Portuguese Natural Language Tasks](http://ceur-ws.org/Vol-2583/3_DLB.pdf)
=================

This is the source code for the model that has been submitted by the Deep Learning Brasil team to the 
[II Evaluation of Semantic Textual Similarity and Textual Inference in Portuguese](https://sites.google.com/view/assin2/english) 
that happened in 2019 during the [Symposium in Information and Human Language Technology](http://comissoes.sbc.org.br/ce-pln/stil2019/).

At that time, a submission produced by this code achieved the best scores among all submissions for the entailment task. This particular submission can be reproduced by the file `settings/roberta-bert-multilingual-5folds.yml`. 

We described our approach in the paper “[Multilingual Transformer Ensembles for Portuguese Natural Language Tasks](http://ceur-ws.org/Vol-2583/3_DLB.pdf)”.

* [STIL 2019 Presentation](https://github.com/ruanchaves/assin/blob/master/STIL2019_presentation.pdf)

* [PROPOR 2020 Presentation](https://github.com/ruanchaves/assin/blob/master/PROPOR2020_presentation.pdf)

* [Proceedings of the ASSIN 2 Shared Task: Evaluating Semantic Textual Similarity and Textual Entailment in Portuguese
co-located with XII Symposium in Information and Human Language Technology (STIL 2019)](http://ceur-ws.org/Vol-2583/)

* [Multilingual Transformer Ensembles for Portuguese Natural Language Tasks](http://ceur-ws.org/Vol-2583/3_DLB.pdf)

The complete test results of all our experiments are in the file [`reports/full_report.csv`](reports/full_report.csv). 

## Setup

Assuming you have already installed Docker and [nvidia-docker](https://github.com/NVIDIA/nvidia-docker) on your system, clone this repository and run:

```
PREFIX=roberta-portuguese CUDA_VISIBLE_DEVICES=0 bash scripts/start.sh
```

or, if you can only run Docker as root:

```
sudo PREFIX=roberta-portuguese CUDA_VISIBLE_DEVICES=0 bash scripts/start.sh
```

This command will perform all fine-tuning procedures specified on the configuration files in the `settings` folder over all datasets ( `assin2`, `assin-ptpt` and `assin-ptbr` ). Configuration files with a name that does not start with `PREFIX` will be ignored. If the image `ruanchaves/assin:2.0` does not exist, it will be created.

Depending on your resources, you may want change the maximum amount of parallel workers allowed on each configuration file. Generally speaking, each worker will consume at most 8 gigabytes of GPU memory.

All intermediate files are deleted by default, and the final submissions will be stored in a folder called `submission_<timestamp>`, where `<timestamp>` stands for the system time when the fine-tuning procedure started.


## Associated Repositories

You may want to take a look at the [ruanchaves/elmo](https://github.com/ruanchaves/elmo) repository. It contains tests which were performed with ELMo and Portuguese word embeddings on the ASSIN datasets.

## Citation

```
@inproceedings{rodrigues_assin2,
Author = {Ruan Chaves Rodrigues and Jéssica Rodrigues da Silva and Pedro Vitor Quinta de Castro and Nádia Félix Felipe da Silva and Anderson da Silva Soares },
Booktitle = {Proceedings of the {ASSIN 2} Shared Task: {E}valuating {S}emantic {T}extual {S}imilarity and {T}extual {E}ntailment in {P}ortuguese},
Pages = {[In this volume]},
Publisher = {CEUR-WS.org},
Series = {{CEUR} Workshop Proceedings},
Title = {Multilingual Transformer Ensembles for Portuguese Natural Language Tasks},
Year = {2020}}
```
