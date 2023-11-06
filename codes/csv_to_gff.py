# tab_to_gff.py

def convert_to_gff(input_file, output_file):
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        for line in infile:
            columns = line.strip().split('\t')
            start = columns[0]
            end = columns[1]
            sequence = columns[3]
            strand = columns[6]
            gene_name = columns[8]
            attributes = f"ID={gene_name};Name={gene_name}"
            gff_entry = f"{sequence}\t.\tgene\t{start}\t{end}\t.\t{strand}\t.\t{attributes}"
            outfile.write(gff_entry + "\n")
    print(f"Conversion completed. GFF data saved to {output_file}")

if __name__ == "__main__":
    input_file = "../raw_data/gff3/GTAC-139491-MA-3.HNL3JDSX5_CTCTGTTCGG-TCTTAGGCCT_L002_R1_filtered_output.txt"
    output_file = "../raw_data/gff3/GTAC-139491-MA-3.HNL3JDSX5_CTCTGTTCGG-TCTTAGGCCT_L002_R1_filtered_output.gff"
    convert_to_gff(input_file, output_file)
