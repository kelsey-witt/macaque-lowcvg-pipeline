# macaque-lowcvg-pipeline

This workflow was developed to perform population genomics analyses on low-coverage ancient genomes (even less than 5% of the genome). It uses genotype likelihoods to call SNPs using ANGSD, and calculates a number of metrics useful for population genetics, including heterozygosity and FST, and generates PCA and admixture plots, as well as phylogenetic trees. The workflow includes commands for ANGSD and all other programs, as well as python scripts that are used to filter or re-format the data for additional analyses.

The full workflow is outlined in "Angsd Low-Coverage SNP Pipeline.txt", and all python scripts written for the workflow are included here.

Required software:
* Python3 
* ANGSD
* pcangsd (PCA/Admixture plots)
* RAxML (maximum likelihood trees)
* TASSEL (neighbor joining trees)

Please see the [angsd documentation](http://www.popgen.dk/angsd/index.php/ANGSD#Overview) for a thorough explanation of angsd and its options!

Contact: Kelsey E. Witt (kelsey_witt_dillon@brown.edu)
