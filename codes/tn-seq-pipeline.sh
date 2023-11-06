##########################################################################################################################
############## STEP 1: CONVERT THE FASTQ TO WIG FORMST; as required in transit
##########################################################################################################################

python src/tpp.py -bwa "../Bioinformatics_projects/Tn-seq/bwa-0.7.17/bwa" \
    -ref "../Bioinformatics_projects/Tn-seq/raw_data/reference.fasta" \
    -reads1 "../Bioinformatics_projects/Tn-seq/subset_fastq/GTAC-139491-MA-1.HNL3JDSX5_TGATTCACCT-GAGTTCGAAC_L002_R2.fastq.gz" \
    -output "../Bioinformatics_projects/Tn-seq/test/GTAC-139491-MA-1.HNL3JDSX5_TGATTCACCT-GAGTTCGAAC_L002_R2" \
     -protocol Tn5 -replicon-ids auto -primer GAGTTCGAAC

#-reads2 "../Bioinformatics_projects/Tn-seq/raw_data/GTAC-139491-MA-1.HNL3JDSX5_TGATTCACCT-GAGTTCGAAC_L002_R2.fastq.gz" \

# PRIMERS THAT SEEM TO WORK
#CCTAGGCGGCCTTAATTAAAGATGTGTATAAGAG

##########################################################################################################################
##############  STEP 2: CONVERT THE gff3 TO prot_table; as required in transit 
##########################################################################################################################

#  python src/transit.py convert gff_to_prot_table ../Bioinformatics_projects/Tn-seq/raw_data/gff3/uniprotkb_proteome_UP000002695_2023_11_06.gff \
#  ../Bioinformatics_projects/Tn-seq/raw_data/prot_tables/uniprotkb_proteome_UP000002695_2023_11_06.prot_table




##########################################################################################################################
##############  STEP 3: CREATE COMBINED WIG FILE
##########################################################################################################################










##########################################################################################################################
##############  STEP 3: ANOVA
##########################################################################################################################

#python src/transit.py  anova  <combined wig file> <samples_metadata file> <annotation .prot_table> <output file>

# python src/transit.py  anova ../Bioinformatics_projects/Tn-seq/test/GTAC-139491-MA-3.HNL3JDSX5_CTCTGTTCGG-TCTTAGGCCT_L002_R1.wig \
#     ../Bioinformatics_projects/Tn-seq/raw_data/samples_metadata/sample_metadata.txt\
#     ../Bioinformatics_projects/Tn-seq/raw_data/gff3/GTAC-139491-MA-3.HNL3JDSX5_CTCTGTTCGG-TCTTAGGCCT_L002_R1_filtered_output.txt \
#     ../Bioinformatics_projects/Tn-seq/test/GTAC-139491-MA-3.HNL3JDSX5_CTCTGTTCGG-TCTTAGGCCT_L002_R1_anova
