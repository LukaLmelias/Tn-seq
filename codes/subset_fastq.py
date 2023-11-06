
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
            with gzip.open(input_file, "rt") as input_handle, gzip.open(output_file, "wt") as output_handle:
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
    input_directory = "../raw_data"  # Define your input directory path
    output_directory = "../subset_fastq"  # Define your output directory path
    subset_size = 4000  # how many lines to pick

    # run the function to subset
    subset_fastq_files(input_directory, output_directory, subset_size)

if __name__ == "__main__":
    main()

