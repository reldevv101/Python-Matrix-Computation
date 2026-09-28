# Matrix Computation Benchmark

Fondasi awal proyek untuk membandingkan kinerja komputasi matriks. Tahap ini
hanya berisi **perkalian matriks sequential** dalam program konsol—belum ada
multiprocessing, MPI/distributed computing, maupun GUI.

## Kebutuhan

- Python 3.10 atau lebih baru
- Tidak ada dependency pihak ketiga

## Menjalankan

Dari folder proyek, jalankan:

```powershell
py -3 main.py --size 100
```

Opsi yang tersedia:

- `--size`: ukuran matriks persegi (default: `100`)
- `--seed`: seed pembangkit data agar hasil dapat diulang (default: `42`)

Contoh:

```powershell
py -3 main.py --size 250 --seed 7
```

Program membuat dua matriks acak berukuran `N x N`, menghitung hasil `A x B`
secara sequential, lalu menampilkan waktu komputasi serta checksum hasil.
Checksum berguna sebagai pengecekan sederhana saat kelak membandingkan hasil
sequential, parallel, dan distributed.

## Pengujian

```powershell
$env:PYTHONPATH = "src"
py -3 -m unittest discover -s tests -v
```

## Struktur

```text
main.py               entry point praktis
src/matrix_benchmark/ kode aplikasi
tests/                pengujian dasar
README.md             cara memakai proyek
pyproject.toml        metadata dan instalasi opsional
```
