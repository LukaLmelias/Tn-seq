import pysam

def sam_to_gff3(sam_file, gff3_file):
    with pysam.AlignmentFile(sam_file, "r") as sam, open(gff3_file, "w") as gff3:
        for alignment in sam:
            # Extract relevant information from the SAM alignment
            seqid = alignment.reference_name  # Chromosome name
            source = "gene"  # Replace with your desired source
            type = "alignment"  # Replace with your desired type
            start = alignment.reference_start + 1  # 1-based start position
            end = alignment.reference_end  # End position
            score = "."  # No score information in SAM
            strand = "+" if not alignment.is_reverse else "-"  # Strand information
            phase = "."  # No phase information in SAM
            read_name = alignment.query_name

            # Create the GFF3 entry
            gff3_entry = f"{seqid}\t{source}\t{type}\t{start}\t{end}\t{score}\t{strand}\t{phase}\tID={read_name};Name={read_name}"

            # Write the GFF3 entry to the file
            gff3.write(gff3_entry + "\n")
            
if __name__ == "__main__":
    sam_file = "/mnt/c/Users/lmeli/Desktop/Bioinformatics_projects/Tn-seq/test/GTAC-139491-MA-1.HNL3JDSX5_TGATTCACCT-GAGTTCGAAC_L002_R2.sam"  # Replace with the path to your SAM file
    gff3_file = "/mnt/c/Users/lmeli/Desktop/Bioinformatics_projects/Tn-seq/raw_data/gff3/GTAC-139491-MA-1.HNL3JDSX5_TGATTCACCT-GAGTTCGAAC_L002_R2.gff3"  # Replace with the desired GFF3 output file name

    sam_to_gff3(sam_file, gff3_file)
