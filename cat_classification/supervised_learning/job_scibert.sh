#! /bin/bash

#SBATCH --job-name=SciBert
#SBATCH -o r_out%j.out
#SBATCH -e r_err%j.err

#SBATCH --mail-user=niting@email.sc.edu
#SBATCH --mail-type=ALL

#SBATCH -p v100-16gb-hiprio
#SBATCH --gres=gpu:1

module load python3/anaconda/2021.07 gcc/12.2.0 cuda/12.1
source activate /home/niting/.conda/envs/lit-cat

pip install imbalanced-learn

echo $CONDA_DEFAULT_ENV

#Run script
hostname
python3 paper_categorization_scibert.py

#Exit the conda system
conda deactivate