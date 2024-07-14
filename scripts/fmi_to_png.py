import click
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import math
from dataclasses import dataclass


@dataclass
class FmiGraph:
    vertices: np.ndarray
    edges: np.ndarray

    def from_fmi_file(filename):
        with open(filename, "r") as infile:
            while True:
                line = infile.readline().strip()
                if not line.startswith("#"):
                    break

            num_vertices = infile.readline().strip()
            num_edges = infile.readline().strip()

            vertices = np.empty([int(num_vertices), 2], dtype=np.float64)
            edges = np.empty([int(num_edges), 3], dtype=np.uint32)
            graph = FmiGraph(vertices, edges)

            for vertex_id in tqdm(
                range(int(num_vertices)), desc="Processing vertices", leave=False
            ):
                vertex_data = infile.readline().split()
                longitude = float(vertex_data[2])
                latitude = float(vertex_data[3])
                graph.vertices[vertex_id][0] = longitude
                graph.vertices[vertex_id][1] = latitude

            for edge_id in tqdm(
                range(int(num_edges)), desc="Processing edges", leave=False
            ):
                edge_data = infile.readline().split()
                tail = int(edge_data[0])
                head = int(edge_data[1])
                weight = int(edge_data[2])
                graph.edges[edge_id][0] = tail
                graph.edges[edge_id][1] = head
                graph.edges[edge_id][2] = weight

            return graph

    def to_fmi_file(self, filename):
        with open(filename, "w") as outfile:
            for _ in range(4):
                outfile.write(f"#\n")
            outfile.write(f"\n")

            outfile.write(f"{len(self.vertices)}\n")
            outfile.write(f"{len(self.edges)}\n")

            for id, (lon, lat) in enumerate(
                tqdm(self.vertices, desc="Writing vertices", leave=False)
            ):
                outfile.write(f"{id} {id} {lon} {lat}\n")

            for tail, head, weight in tqdm(
                self.edges, desc="Writing edges", leave=False
            ):
                outfile.write(f"{tail} {head} {weight}\n")


def equirectangular_projection(
    width, height, lat, lon, min_lat, max_lat, min_lon, max_lon
):
    x = (lon - min_lon) / (max_lon - min_lon) * width
    y = (max_lat - lat) / (max_lat - min_lat) * height
    return int(x), int(y)


def mercator_projection(width, height, lat, lon, min_lat, max_lat, min_lon, max_lon):
    def mercator_y(lat):
        return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))

    min_merc_y = mercator_y(min_lat)
    max_merc_y = mercator_y(max_lat)

    x = (lon - min_lon) / (max_lon - min_lon) * width
    y = (max_merc_y - mercator_y(lat)) / (max_merc_y - min_merc_y) * height
    return int(x), int(y)


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
    "-v",
    "--draw_vertices",
    is_flag=True,
    required=False,
    type=click.BOOL,
    help="Output file path.",
)
@click.option(
    "-e",
    "--draw_edges",
    is_flag=True,
    required=False,
    type=click.BOOL,
    help="Output file path.",
)
def process_file(input_file, output_file, draw_vertices, draw_edges):
    """
    Processes the input file and writes to the output file.
    """
    graph = FmiGraph.from_fmi_file(input_file)
    graph.to_fmi_file("test.fmi")

    dots_per_degree = 300

    max_longitude = np.max(graph.vertices[:, 0])
    min_longitude = np.min(graph.vertices[:, 0])

    max_latitude = np.max(graph.vertices[:, 1])
    min_latitude = np.min(graph.vertices[:, 1])

    width = int((max_longitude - min_longitude) * dots_per_degree)
    height = int((max_latitude - min_latitude) * dots_per_degree)

    # Create a new image with white background
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    if draw_vertices:
        for lon, lat in tqdm(graph.vertices, desc="Drawing vertices", leave=False):
            x, y = mercator_projection(
                width,
                height,
                lat,
                lon,
                min_latitude,
                max_latitude,
                min_longitude,
                max_longitude,
            )

            dot_radius = 1
            dot_color = "red"

            draw.ellipse(
                (
                    x - dot_radius,
                    y - dot_radius,
                    x + dot_radius,
                    y + dot_radius,
                ),
                fill=dot_color,
            )

    if draw_edges:
        for tail, head, _weight in tqdm(graph.edges, desc="Drawing edges", leave=False):
            tail_x, tail_y = mercator_projection(
                width,
                height,
                graph.vertices[tail][1],
                graph.vertices[tail][0],
                min_latitude,
                max_latitude,
                min_longitude,
                max_longitude,
            )
            head_x, head_y = mercator_projection(
                width,
                height,
                graph.vertices[head][1],
                graph.vertices[head][0],
                min_latitude,
                max_latitude,
                min_longitude,
                max_longitude,
            )
            draw.line((tail_x, tail_y, head_x, head_y), fill="black", width=1)

    image.save(output_file)


if __name__ == "__main__":
    process_file()
