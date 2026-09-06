"""
Uniform Cost Search dengan state ter-augmentasi untuk masalah multi-agenda.

State di-augmentasi dengan frozenset agenda yang sudah selesai karena
shortest-path biasa tidak menjamin semua agenda terpenuhi — dua jalur
yang tiba di lokasi yang sama bisa berbeda dalam agenda yang sudah
dikunjungi, sehingga keduanya harus dieksplorasi secara terpisah.
"""

import heapq
from typing import Optional


def ucs(
    graph: dict[str, list[tuple[str, int]]],
    start: str,
    agendas: frozenset[str],
    trace_sink: Optional[list] = None,
) -> Optional[tuple[int, list[str]]]:
    """
    Uniform Cost Search dengan state (lokasi, agenda_selesai).

    Args:
        graph: adjacency list {node: [(neighbor, weight), ...]}
        start: node awal dan node tujuan akhir
        agendas: himpunan node yang wajib dikunjungi
        trace_sink: jika diberikan, setiap langkah ekspansi di-append ke list ini

    Returns:
        (total_cost, path) jika ditemukan, None jika tidak ada solusi.
    """
    for node in agendas:
        if node not in graph:
            raise ValueError(f"Node agenda '{node}' tidak ditemukan di graf.")

    # counter jadi tie-breaker urutan heap saat cost sama, karena frozenset/list
    # di tuple tidak bisa dibandingkan langsung oleh heapq
    counter = 0
    # start bisa juga jadi agenda (mis. agenda = start), jadi langsung tandai selesai
    initial_done = agendas & {start}
    frontier: list[tuple[int, int, str, frozenset, list[str]]] = [
        (0, counter, start, initial_done, [start])
    ]

    explored: set[tuple[str, frozenset]] = set()
    nodes_expanded = 0
    max_frontier = 1

    while frontier:
        max_frontier = max(max_frontier, len(frontier))
        # heap terurut berdasarkan cost (elemen pertama tuple), jadi pop selalu ambil node termurah
        cost, _, loc, done, path = heapq.heappop(frontier)

        # Goal test saat di-pop (bukan saat push) — menjamin optimalitas UCS,
        # karena elemen yang di-pop dijamin punya cost minimum di antara yang tersisa
        if loc == start and done == agendas:
            if trace_sink is not None:
                trace_sink.append({
                    "step": nodes_expanded + 1,
                    "expanded_state": {"location": loc, "done": sorted(done)},
                    "g": cost,
                    "frontier": [],
                    "explored_count": len(explored),
                    "is_goal": True,
                })
            print(f"[UCS Stats] Node di-expand: {nodes_expanded}, Frontier maks: {max_frontier}")
            return cost, path

        state = (loc, done)
        if state in explored:
            # state (lokasi, agenda_selesai) yang sama bisa masuk frontier lebih dari
            # sekali lewat jalur berbeda; skip duplikat yang sudah pernah di-expand
            continue
        explored.add(state)
        nodes_expanded += 1

        for neighbor, weight in graph.get(loc, []):
            new_cost = cost + weight
            # tandai agenda selesai jika neighbor adalah salah satu node agenda
            new_done = done | ({neighbor} & agendas)
            new_state = (neighbor, new_done)
            if new_state not in explored:
                counter += 1
                heapq.heappush(
                    frontier,
                    (new_cost, counter, neighbor, new_done, path + [neighbor]),
                )

        if trace_sink is not None:
            snapshot = sorted(
                [{"location": item[2], "done": sorted(item[3]), "g": item[0]} for item in frontier],
                key=lambda x: x["g"],
            )
            trace_sink.append({
                "step": nodes_expanded,
                "expanded_state": {"location": loc, "done": sorted(done)},
                "g": cost,
                "frontier": snapshot,
                "explored_count": len(explored),
                "is_goal": False,
            })

    return None
