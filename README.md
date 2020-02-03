ASSIN 2
=================

This is the source code for the model that has been submitted by the Deep Learning Brasil team to the 
[II Evaluation of Semantic Textual Similarity and Textual Inference in Portuguese](https://sites.google.com/view/assin2/english) 
that happened in 2019 during the [Symposium in Information and Human Language Technology](http://comissoes.sbc.org.br/ce-pln/stil2019/).

At that time, a submission produced by this code achieved the best scores among all submissions for the entailment task. This particular submission can be reproduced by the file `settings/roberta-bert-multilingual-5folds.yml`. 

You may also want to read the current version of [our presentation slides](https://github.com/ruanchaves/assin/blob/master/STIL2019_presentation.pdf). A paper and a brief blog post on our findings are currently in the works.

## Setup

Assuming you have already installed Docker and [nvidia-docker](https://github.com/NVIDIA/nvidia-docker) on your system, clone this repository and run:

```
PREFIX=roberta-portuguese CUDA_VISIBLE_DEVICES=0 bash scripts/start.sh
```

or, if you can only run Docker as root:

```
sudo PREFIX=roberta-portuguese CUDA_VISIBLE_DEVICES=0 bash scripts/start.sh
```

This command will perform all fine-tuning procedures specified on the configuration files in the `settings` folder over all datasets ( `assin2`, `assin-ptpt` and `assin-ptbr` ). Configuration files with a name that does not start with `PREFIX` will be ignored.

Depending on your resources, you may want change the maximum amount of parallel workers allowed on each configuration file. Generally speaking, each worker will consume at most 8 gigabytes of GPU memory.

All intermediate files are deleted by default, and the final submissions will be stored in a folder called `submission_<timestamp>`, where `<timestamp>` stands for the system time when the fine-tuning procedure started.

## Citation

A paper about our findings is planned to be released this year. 
Until then, you may cite this very repository: 

```
@misc{Rodrigues2019,
  author = {Ruan Chaves Rodrigues and Jéssica Rodrigues da Silva and Pedro Vitor Quinta de Castro and Nádia Félix Felipe da Silva and Anderson da Silva Soares},
  title = {ASSIN},
  year = {2019},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/ruanchaves/assin}},
  commit = {f8c3f185fb3bcd106c8a0e5a12d9ef2c6119ec74}
}
```
