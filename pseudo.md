# Pseudocode: Uniform Cost Search (UCS) Rute Harian Kampus

## Definisi State

```
State = (lokasi: string, agenda_selesai: set<string>)

Initial State = (START, {})
Goal State    = (START, {semua agenda wajib})
```

> State harus di-augmentasi dengan `agenda_selesai` karena dua jalur yang
> tiba di lokasi yang sama bisa berbeda dalam agenda yang sudah dikunjungi.
> Tanpa augmentasi ini, algoritma bisa berhenti terlalu cepat tanpa
> memastikan semua agenda terpenuhi.

---

## Pseudocode UCS

```
function UCS(graph, start, agendas):

    // Validasi input
    for setiap agenda in agendas:
        if agenda tidak ada di graph:
            error "Node agenda tidak ditemukan"

    // Inisialisasi frontier sebagai priority queue (min-heap)
    // Elemen: (g_cost, lokasi, agenda_selesai, path)
    frontier ← priority_queue
    frontier.push(cost=0, loc=start, done={}, path=[start])

    // Explored set mencatat STATE yang sudah di-expand
    explored ← empty set

    while frontier tidak kosong:

        // Ambil state dengan g_cost terkecil
        (cost, loc, done, path) ← frontier.pop_min()

        // GOAL TEST: dilakukan saat di-pop, bukan saat di-generate
        // → menjamin optimalitas karena cost sudah pasti minimal
        if loc == start AND done == agendas:
            return (cost, path)

        state ← (loc, done)

        // Lewati jika state sudah pernah di-expand
        if state in explored:
            continue

        explored.add(state)

        // Ekspansi: kunjungi semua tetangga
        for setiap (neighbor, weight) in graph[loc]:
            new_cost ← cost + weight
            new_done ← done ∪ ({neighbor} ∩ agendas)  // catat agenda jika tiba di sana
            new_state ← (neighbor, new_done)

            if new_state tidak in explored:
                frontier.push(cost=new_cost, loc=neighbor,
                              done=new_done, path=path+[neighbor])

    return NULL  // tidak ada solusi
```

---

## Pseudocode Main

```
function MAIN():
    result ← UCS(GRAPH, START, AGENDAS)

    if result == NULL:
        print "Tidak ditemukan rute"
        return

    (total_cost, path) ← result

    print "Rute lengkap: " + path.join(" → ")
    print "Total waktu: " + total_cost + " menit"

    agenda_order ← [node for node in path if node in AGENDAS]
    print "Urutan agenda: " + agenda_order
```

---

## Ilustrasi Alur Kerja UCS

```
Frontier (min-heap)          Explored
─────────────────────        ────────────────────────────
[(0, GerbangUtama, {})]      {}

Pop → (0, GerbangUtama, {})   ← bukan goal (done kosong)
Push tetangga J1 (cost=3), J2 (cost=5)

[(3, J1, {}), (5, J2, {})]   {(GerbangUtama, {})}

Pop → (3, J1, {})
Push tetangga: GerbangUtama(6), Perpustakaan(7), J3(5)

...eksplorasi berlanjut hingga...

Pop → (35, GerbangUtama, {Perpustakaan, Kantin, GOR})
      ↑ loc == START dan done == semua agenda → GOAL! return 35
```

---

## Kompleksitas

| | Keterangan |
|---|---|
| **State space** | \|lokasi\| × 2^(\|agendas\|) = 8 × 8 = 64 state |
| **Time** | O(S log S) di mana S = jumlah state yang di-expand |
| **Space** | O(S) untuk frontier + explored |
| **Optimalitas** | Dijamin selama semua bobot edge ≥ 0 |
