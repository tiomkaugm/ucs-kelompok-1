import json
import os
import sys

# Menambahkan direktori 'src' ke sys.path agar modul map dan utils terbaca
SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from map.campus_map import AGENDAS, COORDS, GRAPH, START
from utils.ucs import ucs


def generate_trace():
    trace_log = []
    result = ucs(GRAPH, START, AGENDAS, trace_sink=trace_log)

    if result is None:
        print("Solusi rute tidak ditemukan!")
        return

    total_cost, path = result

    # Parsing sisi graf (edges) tanpa duplikasi arah
    edges_data = []
    seen_edges = set()
    for u, neighbors in GRAPH.items():
        for v, w in neighbors:
            edge_key = tuple(sorted([u, v]))
            if edge_key not in seen_edges:
                seen_edges.add(edge_key)
                edges_data.append({"from": u, "to": v, "weight": w})

    # Parsing koordinat simpul (nodes)
    nodes_data = [
        {"id": node_id, "x": coords[0], "y": coords[1]}
        for node_id, coords in COORDS.items()
    ]

    output_payload = {
        "start": START,
        "agendas": list(AGENDAS),
        "graph": {"nodes": nodes_data, "edges": edges_data},
        "result": {"total_cost": total_cost, "path": path},
        "trace": trace_log,
    }

    output_path = os.path.join(os.path.dirname(__file__), "trace.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_payload, f, indent=2, ensure_ascii=False)

    print(f"[OK] Berhasil membuat trace.json di: {output_path}")
    print(f"[Info] Total Cost: {total_cost} menit | Jalur: {' -> '.join(path)}")


if __name__ == "__main__":
    generate_trace()