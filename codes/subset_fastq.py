
import os
import gzip

def subset_fastq_files(input_directory, output_directory, subset_size):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    # Iterate over the gzipped FASTQ files in the input directory
    for filename in os.listdir(input_directory):
        if filename.endswith(".fastq.gz") or filename.endswith(".fq.gz"):
            input_file = os.path.join(input_directory, filename)
            output_file = os.path.join(output_directory, filename)

            # Create a subset of the gzipped FASTQ file
            with gzip.open(input_file, "rt") as input_handle, open(output_file, "w") as output_handle:
                records = []
                record_count = 0

                for line in input_handle:
                    records.append(line)
                    if len(records) == 4:
                        record_count += 1
                        if record_count <= subset_size:
                            output_handle.writelines(records)
                        records = []

            print(f"Created subset file: {output_file}")

    print("Subset FASTQ files have been created.")


def main():

    # define input directory (fixed as current directory)
    input_directory = os.getcwd()

    output_directory = os.path.join(input_directory, "subset_fastq") # new directory to store the subset

    subset_size = 400 # how many lines to pick

    # run the function to subset
    subset_fastq_files(input_directory, output_directory, subset_size)

if __name__ == "__main__":
    main()

