from tqdm import tqdm
import numpy as np
from dataclasses import dataclass


@dataclass
class FmiGraph:
    vertices: np.ndarray
    edges: np.ndarray

    def vertices_and_edges_from_fmi_file(filename):
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

    def vertices_from_fmi_file(filename):
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
