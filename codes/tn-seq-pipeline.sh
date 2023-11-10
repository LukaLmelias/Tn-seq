##########################################################################################################################
############## STEP 1: CONVERT THE FASTQ TO WIG FORMST; as required in transit
##########################################################################################################################

# python src/tpp.py -bwa "../Bioinformatics_projects/Tn-seq/bwa-0.7.17/bwa" \
#     -ref "../Bioinformatics_projects/Tn-seq/raw_data/reference.fasta" \
#     -reads1 /mnt/c/Users/lmeli/Desktop/Bioinformatics_projects/Tn-seq/subset_fastq/GTAC-139491-MA-3.HNL3JDSX5_CTCTGTTCGG-TCTTAGGCCT_L002_R1.fastq.gz \
#     -output /mnt/c/Users/lmeli/Desktop/Bioinformatics_projects/Tn-seq/test/GTAC-139491-MA-3.HNL3JDSX5_CTCTGTTCGG-TCTTAGGCCT_L002_R1 \
#      -protocol Tn5 -replicon-ids auto -primer CCTAGGCGGCCTTAATTAAAGATGTGTATAAGAG
#-reads2 "../Bioinformatics_projects/Tn-seq/raw_data/GTAC-139491-MA-1.HNL3JDSX5_TGATTCACCT-GAGTTCGAAC_L002_R2.fastq.gz" \

# PRIMERS THAT SEEM TO WORK (turns out: the transposon terminus appears in the prefix of read1 reads, and barcodes are embedded in read2 reads.)
# primer for reads1: CCTAGGCGGCCTTAATTAAAGATGTGTATAAGAG
# primer for reads2: GGGGGGGGGGGGGGGG
# this is the one used in the paer: GACAG; "he TPP searched for the 19 nucleotide inverted repeat (IR) sequence and identified five nucleotides (GACAG) at the end of the IR sequence, allowing one nucleotide mismatch."
##########################################################################################################################
##############  STEP 2: CONVERT THE gff3 TO prot_table; as required in transit 
##########################################################################################################################

#  python src/transit.py convert gff_to_prot_table ../Bioinformatics_projects/Tn-seq/raw_data/gff3/all_features_reference.gff3 \
#  ../Bioinformatics_projects/Tn-seq/raw_data/prot_tables/all_features_reference.prot_table




##########################################################################################################################
##############  STEP 3: RUN THE RESAMPLING STEP
##########################################################################################################################
#  python3 transit.py resampling <comma-separated .wig control files> <comma-separated .wig experimental files> <annotation .prot_table or GFF3> <output file> [Optional Arguments]



python src/transit.py resampling \
    /mnt/c/Users/lmeli/Desktop/Bioinformatics_projects/Tn-seq/test/GTAC-139491-MA-1.HNL3JDSX5_TGATTCACCT-GAGTTCGAAC_L002_R2.wig \
    /mnt/c/Users/lmeli/Desktop/Bioinformatics_projects/Tn-seq/test/GTAC-139491-MA-2.HNL3JDSX5_CTCACGGTAA-GAGTTCGAAC_L002_R2.wig \
    /mnt/c/Users/lmeli/Desktop/Bioinformatics_projects/Tn-seq/raw_data/prot_tables/reference.prot_table\
    /mnt/c/Users/lmeli/Desktop/Bioinformatics_projects/Tn-seq/test/resampling_conditionally_essential_genes


python src/transit.py resampling \
    /mnt/c/Users/lmeli/Desktop/Bioinformatics_projects/Tn-seq/test/GTAC-139491-MA-1.HNL3JDSX5_TGATTCACCT-GAGTTCGAAC_L002_R2.wig /mnt/c/Users/lmeli/Desktop/Bioinformatics_projects/Tn-seq/test/GTAC-139491-MA-2.HNL3JDSX5_CTCACGGTAA-GAGTTCGAAC_L002_R2.wig /mnt/c/Users/lmeli/Desktop/Bioinformatics_projects/Tn-seq/raw_data/prot_tables/reference.prot_table \
    /mnt/c/Users/lmeli/Desktop/Bioinformatics_projects/Tn-seq/test/resampling_conditionally_essential_genes





#, /mnt/c/Users/lmeli/Desktop/Bioinformatics_projects/Tn-seq/test/GTAC-139491-MA-3.HNL3JDSX5_CTCTGTTCGG-TCTTAGGCCT_L002_R1.wig \


##########################################################################################################################
##############  STEP 3: ANOVA
##########################################################################################################################

#python src/transit.py  anova  <combined wig file> <samples_metadata file> <annotation .prot_table> <output file>

# python src/transit.py  anova ../Bioinformatics_projects/Tn-seq/test/GTAC-139491-MA-3.HNL3JDSX5_CTCTGTTCGG-TCTTAGGCCT_L002_R1.wig \
#     ../Bioinformatics_projects/Tn-seq/raw_data/samples_metadata/sample_metadata.txt\
#     ../Bioinformatics_projects/Tn-seq/raw_data/gff3/GTAC-139491-MA-3.HNL3JDSX5_CTCTGTTCGG-TCTTAGGCCT_L002_R1_filtered_output.txt \
#     ../Bioinformatics_projects/Tn-seq/test/GTAC-139491-MA-3.HNL3JDSX5_CTCTGTTCGG-TCTTAGGCCT_L002_R1_anova
