# map config

# Node constants
START = "Gerbang Utama"
PERPUSTAKAAN = "Perpustakaan"
KANTIN = "Kantin"
GOR = "Gedung Olahraga"

# Agendas yang wajib dikunjungi
AGENDAS: frozenset[str] = frozenset({PERPUSTAKAAN, KANTIN, GOR})

# Graf kampus: adjacency list {node: [(neighbor, weight_menit), ...]}
# Terdapat node persimpangan (J1-J4) agar UCS benar-benar mengeksplorasi jalur alternatif
GRAPH: dict[str, list[tuple[str, int]]] = {
    START:        [("J1", 3), ("J2", 5)],
    "J1":         [(START, 3), (PERPUSTAKAAN, 4), ("J3", 2)],
    "J2":         [(START, 5), (KANTIN, 3), ("J4", 4)],
    "J3":         [("J1", 2), (GOR, 5), (KANTIN, 6), ("J4", 4), (PERPUSTAKAAN, 3)],
    "J4":         [("J2", 4), (GOR, 3), ("J3", 4)],
    PERPUSTAKAAN: [("J1", 4), ("J3", 3)],
    KANTIN:       [("J2", 3), ("J3", 6)],
    GOR:          [("J3", 5), ("J4", 3)],
}

# Koordinat layout (x, y) untuk visualisasi SVG
# viewBox "0 0 640 520", JS menambahkan offset 50px di kedua sisi
COORDS: dict[str, tuple[int, int]] = {
    START:        (60,  330),
    "J1":         (155, 195),
    "J2":         (195, 325),
    "J3":         (285, 140),
    "J4":         (395, 255),
    PERPUSTAKAAN: (190,  50),
    KANTIN:       (310, 375),
    GOR:          (480, 110),
}
