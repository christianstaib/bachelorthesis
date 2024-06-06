from math import ceil
import click
from tqdm import tqdm

@click.command()
@click.option('--input_file')
@click.option('--output_file')
def process_file(input_file, output_file):
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

        for _ in tqdm(range(int(num_vertices))):
            outfile.write(infile.readline())
        

        for _ in tqdm(range(int(num_edges))):
            line = infile.readline()

            new_line = list()

            for number in line.split():
                if "." in number:
                    number = str(int(ceil(float(number))))

                new_line.append(number)

            outfile.write(' '.join(new_line) + '\n')

if __name__ == "__main__":
    process_file()