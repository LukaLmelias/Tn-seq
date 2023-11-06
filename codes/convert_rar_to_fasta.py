import rarfile

def convert_rar_to_fasta(rar_file_path, fasta_file_path):
    rar_archive = rarfile.RarFile(rar_file_path)
    fasta_file = open(fasta_file_path, 'w')

    for file_info in rar_archive.infolist():
        if not file_info.isdir():
            with rar_archive.open(file_info) as file:
                content = file.read().decode('utf-8')
                
            header = f'>{file_info.filename}'  # Customize the header as needed.
            fasta_file.write(header + '\n')
            fasta_file.write(content + '\n')

    fasta_file.close()
    rar_archive.close()

if __name__ == "__main__":
    input_rar_file = "../raw_data/salmonella_typhimurium_14028s_reference_genome_cp001363.rar" # Replace with your RAR file path.
    output_fasta_file = '../raw_data/salmonella_typhimurium_14028s_reference_genome_cp001363.fasta'  # Replace with your desired FASTA file path.
    convert_rar_to_fasta(input_rar_file, output_fasta_file)
