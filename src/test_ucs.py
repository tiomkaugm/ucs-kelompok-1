"""Unit test sederhana untuk fungsi ucs() dengan graf kecil yang bisa diverifikasi manual."""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from utils.ucs import ucs


def test_simple_triangle():
    """
    Graf: A -1- B -1- C -1- A, agenda = {B, C}
    Jalur optimal: A→B→C→A, cost = 3
    """
    graph = {
        "A": [("B", 1), ("C", 1)],
        "B": [("A", 1), ("C", 1)],
        "C": [("B", 1), ("A", 1)],
    }
    result = ucs(graph, "A", frozenset({"B", "C"}))
    assert result is not None
    cost, path = result
    assert cost == 3
    assert path[0] == "A" and path[-1] == "A"
    assert "B" in path and "C" in path
    print("PASS test_simple_triangle")


def test_longer_path_is_chosen_when_cheaper():
    """
    Graf: S -10- A -1- B -1- S, agenda = {A, B}
    Jalur optimal: S→A→B→S, cost = 12
    """
    graph = {
        "S": [("A", 10)],
        "A": [("S", 10), ("B", 1)],
        "B": [("A", 1), ("S", 1)],
    }
    result = ucs(graph, "S", frozenset({"A", "B"}))
    assert result is not None
    cost, _ = result
    assert cost == 12
    print("PASS test_longer_path_is_chosen_when_cheaper")


def test_no_solution():
    """Graf terputus: tidak ada rute yang bisa kembali ke S setelah mengunjungi B."""
    graph = {
        "S": [("A", 1)],
        "A": [("B", 1)],
        "B": [],
    }
    result = ucs(graph, "S", frozenset({"B"}))
    assert result is None
    print("PASS test_no_solution")


def test_trace_sink():
    """trace_sink harus diisi dengan entri per langkah ekspansi."""
    graph = {
        "S": [("A", 1)],
        "A": [("S", 1)],
    }
    sink: list = []
    ucs(graph, "S", frozenset({"A"}), trace_sink=sink)
    assert len(sink) > 0
    assert sink[-1]["is_goal"] is True
    print("PASS test_trace_sink")


if __name__ == "__main__":
    test_simple_triangle()
    test_longer_path_is_chosen_when_cheaper()
    test_no_solution()
    test_trace_sink()
    print("\nSemua test passed.")
