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

    

        # Check if R2 or R1
        R1_pattern = r'_R1\.'
        R2_pattern =r'_R2\.'
        
        primer = ""
        if re.search(R1_pattern, seq):
            primer = read1_primer
        
        elif re.search(R2_pattern, seq):
            primer = read2_primer

        seq_base_name = seq.split("/")[-1].split("_R")[0]
        outputfile = os.path.join(tpp_output_dir, seq_base_name)

        cmd = f"python src/tpp.py -bwa {bwa_path} \
        -ref {reference} -reads1 {seq} \
        -output {outputfile} -protocol {protocol} \
        -replicon-ids {replicon_ids} -primer {primer}"

        print("\n",cmd,"\n")

        #Run the command and capture the output
        output = subprocess.check_output(cmd, shell=True)

                
        # Print the output
        print("\n",output.decode('utf-8'),"\n")


def main():
    parser = argparse.ArgumentParser(description="Runs tpp pipeline")
    
    #raw data directory
    parser.add_argument("-c", "--config_file_path", help="The directory to search for sequence files")

    # #path to reference genome
    # parser.add_argument("-r",  "--reference", help="path to reference genome")

    # # path to bwa excutable
    # parser.add_argument("-b", "--bwa_path", help="path to bwa excutable")

    # # primer1 sequence
    # parser.add_argument("-p1", "--read1_primer", help="primer sequence for read one, also refered as prefix in tpp")

    # # primer2 sequence
    # parser.add_argument("-p2",  "--read2_primer", help="primer sequence for read two, also refered as prefix in tpp")

    
    # # protocol
    # parser.add_argument("-prot",  "--protocol", help="protocol; one of Tn5, Sassetti, Mme1; default is Sassetti")


    # #extract the arguments   
    


    args = parser.parse_args()

    config_path = args.config_file_path

    tpp_params = get_args(config_path)

    print("\n ********** PROVIDED TPP PARAMS **********\n")
    for key, value in tpp_params.items():
        print(f"{key}:\t{value}")

    
    directory_path = tpp_params["raw_data_path"]

    reference = tpp_params["reference"]

    bwa_path = tpp_params["bwa_path"]

    primer1 = tpp_params["read1_primer"]
    primer2 = tpp_params["read2_primer"]
    protocol = tpp_params["protocol"]
    replicon_ids = tpp_params["replicon_id"]


    # ################################## Call the functions


    # 2. run tpp
    run_tpp(raw_data_directory=directory_path,
    bwa_path = bwa_path,
    reference = reference,
    read1_primer = primer1,    
    read2_primer = primer2,    
    protocol = protocol
     )





if __name__ == "__main__":
    main()
