#!/bin/bash
#SBATCH --partition=students-prod
#SBATCH --gres=gpu:2
#SBATCH --gpus=2
#SBATCH --error=models/outputs/models_training_LEDNet_demo.err
#SBATCH --output=models/outputs/models_training_LEDNet_demo.out

python models_training_or_hpo.py --config=demo --model_name=lednet --evaluate=True --n_epochs=20