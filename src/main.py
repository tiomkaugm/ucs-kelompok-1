import json
import os

from map import GRAPH, START, AGENDAS, COORDS
from utils.ucs import ucs


def main() -> None:
    trace_sink: list = []
    result = ucs(GRAPH, START, AGENDAS, trace_sink=trace_sink)

    if result is None:
        print("Tidak ditemukan rute yang memenuhi semua agenda.")
        return

    total_cost, path = result

    print("=== Hasil UCS: Rute Optimal Harian Kampus ===")
    print()
    print("Rute lengkap:")
    print(" → ".join(path))
    print()
    print(f"Total waktu tempuh: {total_cost} menit")
    print()

    agenda_order = [node for node in path if node in AGENDAS]
    print("Urutan agenda dikunjungi:")
    for i, node in enumerate(agenda_order, 1):
        print(f"  {i}. {node}")

    # Export trace.json untuk visualisasi
    nodes = [{"id": k, "x": v[0], "y": v[1]} for k, v in COORDS.items()]

    seen_edges: set[tuple[str, str]] = set()
    edges = []
    for src, neighbors in GRAPH.items():
        for dst, weight in neighbors:
            key = tuple(sorted([src, dst]))
            if key not in seen_edges:
                seen_edges.add(key)
                edges.append({"from": src, "to": dst, "weight": weight})

    output = {
        "graph": {"nodes": nodes, "edges": edges},
        "agendas": sorted(AGENDAS),
        "start": START,
        "result": {"path": path, "total_cost": total_cost},
        "trace": trace_sink,
    }

    visual_dir = os.path.join(os.path.dirname(__file__), "visual")
    os.makedirs(visual_dir, exist_ok=True)
    out_path = os.path.join(visual_dir, "trace.json")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\ntrace.json → {out_path}")
    print("Buka visualisasi:")
    print("  cd src && python -m http.server 8000")
    print("  Lalu buka: http://localhost:8000/visual/visualize.html")


if __name__ == "__main__":
    main()
