import os
import subprocess
import argparse
import re
import json

def get_args(config_file_path):    
    """
    reads the json config file to extract tpp arguments

    returns a dict of args
    """
    # Load configuration from the JSON file
    with open(config_file_path, "r") as config_file:
        config = json.load(config_file)
    return config


def get_primer(read1_primer,read2_primer,file_path):
    """
    assigns primer to read1_primer if R1 and primer to read2_primer if R2
    """
    
    # Check if R2 or R1
    R1_pattern = r'_R1\.'
    R2_pattern =r'_R2\.'
    
    primer = ""
    if re.search(R1_pattern, file_path):
        primer = read1_primer
    
    elif re.search(R2_pattern, file_path):
        primer = read2_primer
    
    return primer

def find_sequence_files(raw_data_directory):
    """
    raw_data_directory: path to the directory containing raw data

    returns a list containing absolute path of fastq, fastq.gz or fasta files
    """

    sequence_files = []    

    for file in os.listdir(raw_data_directory):
    

        # Check if the file extension is in the list of valid extensions
        
        if file.endswith(".fastq") or file.endswith(".fastq.gz") or \
         file.endswith(".fasta"):

            # Construct the absolute path and add it to the list
            
            sequence_files.append(os.path.join(raw_data_directory,file))

    return sequence_files

def run_tpp(raw_data_directory, bwa_path, reference, read1_primer,
    read2_primer,protocol="Sassetti", replicon_ids='auto'):

    
    #get the raw sequences    
    sequence_files = find_sequence_files(raw_data_directory)
     # Print the list of absolute file paths
    print("\n ********** RAW SEQUENCE FILES DETECTED **********\n")
    for file in sequence_files:
        print(file)


    print("\n ********** RUNNING TPP **********\n")
    
    # Create tpp results dir if it doesnt exist
    tpp_output_dir = os.path.join(raw_data_directory, "tpp_results")    
    if not os.path.exists(tpp_output_dir):        
        os.makedirs(tpp_output_dir)



    #add bwa excutable to the bwa path
    bwa_path = os.path.join(bwa_path, "bwa")


    # run tpp for each file:
    for seq in sequence_files:

        primer = get_primer(read1_primer,read2_primer,seq)

        seq_base_name = seq.split("/")[-1].split("_R")[0]
        outputfile = os.path.join(tpp_output_dir, seq_base_name)

        cmd = f"python src/tpp.py -bwa {bwa_path} \
        -ref {reference} -reads1 {seq} \
        -output {outputfile} -protocol {protocol} \
        -replicon-ids {replicon_ids} -primer {primer}"

        print("\n",cmd,"\n")

        #Run the command and capture the output
        subprocess.check_output(cmd, shell=True)
        # delete some uncessarryb tpp output
        delete_notneeded_outputs(raw_data_directory,".reads1")
        delete_notneeded_outputs(raw_data_directory,".trimmed1_failed_trim")

    return tpp_output_dir

def gff3_to_prot_table(gff3_path):
    """
    Convert gff3 to prot_table

    writes to file a new prot_table to same directory as the reference directory
    """
    table_name = gff3_path.split(".gff3")[0]
    prot_table = f"{table_name}.prot_table"

    print("\n ********** CONVERTING gff3 to PROT_TABLE **********\n")
    cmd = f"python src/transit.py convert gff_to_prot_table {gff3_path} {prot_table}"

    print(cmd)
    subprocess.check_output(cmd, shell=True)

    return prot_table

def get_wigs_per_condition(tpp_results_dir_path, group1, group2):
    """
    looks for wig files and separates them according to the treatment/control groups

    returns two lists: wigs in group one and wigs in group2
    """
    wigs = get_wigs(tpp_results_dir_path)    
    wigs1 = []
    wigs2 = []
    for wig in wigs:
        for g1, g2 in zip(group1,group2):
            if g1 in wig:
                wigs1.append(wig)
            elif g2 in wig:
                wigs2.append(wig)
    
    return wigs1,wigs2 



def run_resampling(tpp_results_dir_path,prot_table,group1, group2):
    """
    runs the resampling step of Tn-seq


    """
    #python3 transit.py resampling <comma-separated .wig control files> <comma-separated .wig experimental files> <annotation .prot_table or GFF3> <output file> [Optional Arguments]
    
    
    wigs1,wigs2 = get_wigs_per_condition(tpp_results_dir_path,group1, group2)
    
    print("\n ********** RUNNING RESAMPLING **********\n")
    wigs1_joined, wigs2_joined = ",".join(wigs1), ",".join(wigs2)

    resampling_output_file = os.path.join(tpp_results_dir_path,"resampling_conditionally_essential_genes.txt") 
    prot_table = "/mnt/c/Users/lmeli/Desktop/Bioinformatics_projects/Tn-seq/raw_data/prot_tables/reference.prot_table"
    

    cmd = f"python src/transit.py resampling { wigs1_joined} { wigs2_joined} {prot_table} {resampling_output_file}"
    
    print(cmd)
    subprocess.check_output(cmd, shell=True)
    

    

    return None
def get_wigs(tpp_results_dir_path):
    """
    returns a list with absolute paths of the wig files generated by tpp
    """
    
    print("\n ********** SEARCHING FOR WIG FILES **********\n")
    wigs = [] # to populate with wigs
    for file in os.listdir(tpp_results_dir_path):
        if file.endswith(".wig"):
            
            wigs.append(os.path.join(tpp_results_dir_path, file))
    
    return wigs

def delete_notneeded_outputs(raw_data_path,file_ending):
    """
    Disk management guys!

    remove any specified output of tpp
    """

    tpp_output_dir = os.path.join(raw_data_path, "tpp_results")
    
    for file in os.listdir(tpp_output_dir):
        #print(file)
        if file.endswith(file_ending):
            print("Deleting:", file)
            os.remove(os.path.join(tpp_output_dir,file))
    return None
    


def combine_wigs(tpp_results_dir_path,prot_table):
    """
    searches the wig files in the tpp_results directory 

    runs the transit combine wigs command

    returns the path of the created combined wig file.
    """

    #python transit.py export combined_wig <comma-separated .wig files> <annotation .prot_table> <output file> [-n <norm>]

    wigs = get_wigs(tpp_results_dir_path)

    print("\n ********** COMBINING WIGS **********\n")
    wigs_joined =  ', '.join(wigs)
    output_wig = os.path.join(tpp_results_dir_path, "combined_wig.txt")
    

    cmd = f"python src/transit.py export combined_wig {wigs_joined} {prot_table} {output_wig}"
    
    print(cmd)
    #subprocess.check_output(cmd, shell=True)
    
    
    return None
    





def main():
    parser = argparse.ArgumentParser(description="Runs tpp pipeline")
    
    #raw data directory
    parser.add_argument("-c", "--config_file_path", help="The directory to search for sequence files")

    # #extract the arguments     

    args = parser.parse_args()

    config_path = args.config_file_path

    tpp_params = get_args(config_path)

    print("\n ********** PROVIDED TPP PARAMS **********\n")
    for key, value in tpp_params.items():
        print(f"{key}:\t{value}")

    # tpp params
    directory_path = tpp_params["raw_data_path"]
    reference = tpp_params["reference"]
    bwa_path = tpp_params["bwa_path"]
    primer1 = tpp_params["read1_primer"]
    primer2 = tpp_params["read2_primer"]
    protocol = tpp_params["protocol"]
    replicon_ids = tpp_params["replicon_id"]

    # gff3 to prot table params
    gff3 = tpp_params["gff3"]

    # Experimental conditions conditions
    group1 = tpp_params["condition1"]
    group2 = tpp_params["condition2"]


    # ################################## Call the functions


    # 2. run tpp
    # tpp_results_path = run_tpp(raw_data_directory=directory_path,
    # bwa_path = bwa_path,
    # reference = reference,
    # read1_primer = primer1,    
    # read2_primer = primer2,    
    # protocol = protocol,
    # replicon_ids = replicon_ids
    #  )

    
    # convert gff3 to prot_table
    #prot_table_path = gff3_to_prot_table(gff3)

    # combine the wig files
    # combine_wigs(tpp_results_path,prot_table_path)

    # run resampling
    #run_resampling(tpp_results_path,prot_table_path,group1, group2)







if __name__ == "__main__":
    main()
