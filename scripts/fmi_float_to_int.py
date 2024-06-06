import math
import click
from tqdm import tqdm

@click.command()
@click.option('--input_file', required=True, type=click.Path(exists=True, dir_okay=False), help='Input file path.')
@click.option('--output_file', required=True, type=click.Path(dir_okay=False, writable=True), help='Output file path.')
def process_file(input_file, output_file):
    """
    Processes the input file and writes to the output file.
    """
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        while True:
            line = infile.readline().strip()
            outfile.write(line + "\n")
            if not line.startswith("#"):
                break

        num_vertices = infile.readline().strip()
        num_edges = infile.readline().strip()
        outfile.write(num_vertices + "\n")
        outfile.write(num_edges + "\n")

        for _ in tqdm(range(int(num_vertices)), desc="Processing vertices"):
            outfile.write(infile.readline())
        
        for _ in tqdm(range(int(num_edges)), desc="Processing edges"):
            line = infile.readline()
            new_line = []

            for number in line.split():
                if "." in number:
                    number = str(math.ceil(float(number)))
                new_line.append(number)

            outfile.write(' '.join(new_line) + '\n')

if __name__ == "__main__":
    process_file()
