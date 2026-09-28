# Matrix Computation Benchmark

Fondasi proyek untuk membandingkan kinerja komputasi matriks. Tahap ini berisi
perkalian matriks **sequential** dan **parallel pada satu komputer** dalam
program konsol—belum ada MPI/distributed computing maupun GUI.

## Kebutuhan

- Python 3.10 atau lebih baru
- Tidak ada dependency pihak ketiga

## Menjalankan di konsol

1. Buka PowerShell.
2. Masuk ke folder proyek:

```powershell
cd "C:\Users\USER\Documents\Codex\Python Matrix Computation"
```

3. Jalankan salah satu perintah berikut.

### Sequential

Versi dasar: seluruh perkalian dikerjakan oleh satu proses.

```powershell
py -3 main.py --size 100 --mode sequential
```

### Parallel

Baris pada matriks kiri dibagi ke beberapa proses dalam satu komputer.

```powershell
py -3 main.py --size 250 --mode parallel --workers 4
```

### Perbandingan sequential dan parallel

Ini adalah perintah utama untuk benchmark. Program menjalankan kedua metode
dengan data yang sama, memeriksa kesamaan hasil, lalu menghitung speedup.

```powershell
py -3 main.py --size 250 --mode both --workers 4
```

Gunakan `--seed` yang sama saat membandingkan beberapa percobaan agar matriks
inputnya tetap sama:

```powershell
py -3 main.py --size 500 --seed 7 --mode both --workers 4
```

Opsi yang tersedia:

- `--size`: ukuran matriks persegi (default: `100`)
- `--seed`: seed pembangkit data agar hasil dapat diulang (default: `42`)
- `--mode`: `sequential`, `parallel`, atau `both` (default: `sequential`)
- `--workers`: jumlah proses untuk mode parallel

Tampilkan bantuan singkat dari program kapan saja dengan:

```powershell
py -3 main.py --help
```

Program membuat dua matriks acak berukuran `N x N`, menghitung hasil `A x B`,
lalu menampilkan waktu komputasi serta checksum hasil. Pada mode `both`,
program memastikan hasil parallel sama dengan sequential dan menampilkan
speedup. Checksum juga berguna saat kelak membandingkan dengan MPI/distributed.

### Membaca hasil

Contoh bentuk keluaran mode `both`:

```text
Matrix Computation Benchmark
Ukuran matriks : 250 x 250
Seed           : 7
Sequential     : 0.xxxxxx detik
Checksum       : nilai-yang-sama
Parallel (4 proses): 0.xxxxxx detik
Checksum       : nilai-yang-sama
Speedup        : x.xx
```

- **Waktu sequential**: waktu satu proses menyelesaikan perkalian.
- **Waktu parallel**: waktu saat pekerjaan dibagi ke sejumlah `worker`.
- **Checksum**: harus sama pada kedua metode. Ini menunjukkan hasil
  perhitungannya konsisten.
- **Speedup**: `waktu sequential / waktu parallel`. Nilai di atas `1.00x`
  berarti parallel lebih cepat; nilai di bawah `1.00x` berarti overhead proses
  masih lebih besar daripada keuntungan parallelisme.

Untuk ukuran kecil, parallel sering lebih lambat karena biaya membuat proses
dan mengirim data. Karena itu, uji beberapa ukuran matriks sebelum menarik
kesimpulan.

## Menjalankan tes otomatis

Tes otomatis memeriksa rumus perkalian, validasi input, dan kesamaan hasil
parallel dengan sequential. Jalankan dari folder proyek:

```powershell
$env:PYTHONPATH = "src"
py -3 -m unittest discover -s tests -v
```

Hasil yang diharapkan di bagian akhir adalah:

```text
Ran 7 tests in ...
OK
```

## Catatan untuk pencatatan benchmark

Saat mulai membuat laporan, catat minimal: ukuran matriks, seed, jumlah worker,
waktu sequential, waktu parallel, dan speedup. Jalankan setiap konfigurasi
lebih dari sekali karena waktu dapat berubah akibat aktivitas komputer lain.

## Struktur

```text
main.py               entry point praktis
src/matrix_benchmark/ kode aplikasi
tests/                pengujian dasar
README.md             cara memakai proyek
pyproject.toml        metadata dan instalasi opsional
```
