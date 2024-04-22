# Research data supporting "Accelerated first-principles exploration of functional groups in graphene oxide"

This repository contains code and data supporting the following work:

> Z. El-Machachi, D. Frantzov, A. Nijamudheen, T. Zarrouk, M. A. Caro, V. L. Deringer, _in preparation_ (2024).

The purpose is to enable readers to access the potential models and characterisation code for reproducing the work, and also to create structural models of their own of functionalised graphene sheets ("graphene oxide", GO). 

## Contents

The repository is structured in the following way:

* **Functionalisation code**: The functionalisation code uses four structural parameters (_p_<sub>1</sub> to _p_<sub>4</sub>) to construct initial structural models of GO in a systematic way. 
* **Models**: MACE model files, checkpoints for refitting and fine-tuning, training and testing databases at each iteration and the submission script for training. 
* **Structures**: Structures after the 2 ns anneal from the three MD runs at 900, 1,200 and 1,500 K along with geometry optimised structures. Additional structure from 1.5 ns at 1,500 K is provided as given in Figure 3. 