import click
from tqdm import tqdm


@click.command()
@click.option(
    "-i",
    "--input_file",
    required=True,
    type=click.Path(exists=True, dir_okay=False),
    help="Input file path.",
)
@click.option(
    "-o",
    "--output_file",
    required=True,
    type=click.Path(dir_okay=False, writable=True),
    help="Output file path.",
)
@click.option(
    "-d",
    "--divider",
    type=click.IntRange(min=1),
    default=1,
    help="Value that divides all edge weights.",
)
def process_file(input_file, output_file, divider):
    """
    Processes the input file and writes to the output file.
    """
    try:
        with open(input_file, "r") as infile, open(output_file, "w") as outfile:
            while True:
                line = infile.readline().strip()
                if not line.startswith("#"):
                    break

            num_vertices = infile.readline().strip()
            num_edges = infile.readline().strip()
            outfile.write(num_vertices + "\n")
            outfile.write(num_edges + "\n")

            for _vertex_id in tqdm(
                range(int(num_vertices)), desc="Processing vertices", leave=False
            ):
                vertex_data = infile.readline().split()
                longitude = float(vertex_data[3]) / divider
                latitude = float(vertex_data[2]) / divider
                outfile.write(f"{longitude} {latitude}\n")

            for _edge_id in tqdm(
                range(int(num_edges)), desc="Processing edges", leave=False
            ):
                edge_data = infile.readline().split()
                tail = edge_data[0]
                head = edge_data[1]
                width = 1
                color = 2

                outfile.write(f"{tail} {head} {width} {color}\n")

    except:
        print(f"error in {input_file}")


if __name__ == "__main__":
    process_file()
