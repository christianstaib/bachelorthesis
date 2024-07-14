from graph import FmiGraph
import json
from tqdm import tqdm
import matplotlib.pyplot as plt
import click

graph_file = "../aegaeis-ref-visibility.fmi"
paths_file = "../random_paths.json"
picture_path = "test2.png"


@click.command()
@click.option(
    "-g",
    "--graph_file",
    required=True,
    type=click.Path(exists=True, readable=True),
    help="Input file path.",
)
@click.option(
    "-p",
    "--paths_file",
    required=True,
    type=click.Path(exists=True, readable=True),
    help="Input file path.",
)
@click.option(
    "-d",
    "--diagram_path",
    required=True,
    type=click.Path(writable=True),
    help="Input file path.",
)
def draw_hits(graph_file, paths_file, diagram_path):
    graph = FmiGraph.from_fmi_file(graph_file)

    with open(paths_file) as f:
        d = json.load(f)
    paths = [x["vertices"] for x in d]

    hits = [0 for _ in range(graph.vertices.shape[0])]
    for path in tqdm(paths):
        for v in path:
            hits[v] += 1

    max_hits = max(hits)
    for i in range(len(hits)):
        hits[i] /= max_hits

    min_lon = min(graph.vertices[:, 0]) / 100000
    max_lon = max(graph.vertices[:, 0]) / 100000
    min_lat = min(graph.vertices[:, 1]) / 100000
    max_lat = max(graph.vertices[:, 1]) / 100000

    diff_lon = max_lon - min_lon
    diff_lat = max_lat - min_lat

    fig, ax = plt.subplots()
    fig.set_dpi(200)

    fig.set_size_inches(diff_lon, diff_lat)

    plt.scatter(x=graph.vertices[:, 0], y=graph.vertices[:, 1], s=0.1, c="black")
    plt.scatter(
        x=graph.vertices[:, 0], y=graph.vertices[:, 1], s=0.75, alpha=hits, c="red"
    )

    plt.savefig(diagram_path)


if __name__ == "__main__":
    draw_hits()
