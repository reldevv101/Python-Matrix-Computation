# Menjalankan MPI pada Dua Komputer Windows

Panduan ini menggunakan satu komputer sebagai **master** yang menjalankan
perintah `mpiexec`, dan satu komputer sebagai **worker**. Aplikasi matrix
benchmark yang sama akan dijalankan sebagai proses MPI pada keduanya.

## 1. Siapkan kedua komputer

Di master dan worker, lakukan hal yang sama:

1. Hubungkan keduanya ke jaringan lokal yang sama.
2. Pasang versi Python, Microsoft MPI (MS-MPI), dan `mpi4py` yang sama.
3. Letakkan salinan project pada path yang sama, misalnya:

   ```text
   C:\Users\USER\Documents\Codex\Python Matrix Computation
   ```

4. Buka PowerShell dan verifikasi:

   ```powershell
   mpiexec -n 2 py -3 -m mpi4py.bench helloworld
   ```

Perintah verifikasi tersebut dilakukan lokal pada masing-masing komputer.

## 2. Catat nama komputer

Di masing-masing komputer, jalankan:

```powershell
hostname
```

Catat hasilnya sebagai `NAMA_MASTER` dan `NAMA_WORKER`. Dari master, pastikan
worker dapat ditemukan di jaringan:

```powershell
ping NAMA_WORKER
```

## 3. Uji dua komputer

Di master, buka PowerShell pada folder project dan jalankan perintah berikut.
Ganti kedua placeholder dengan nama komputer Anda:

```powershell
mpiexec /hosts 2 NAMA_MASTER 1 NAMA_WORKER 1 /wdir "C:\Users\USER\Documents\Codex\Python Matrix Computation" py -3 -m mpi4py.bench helloworld
```

Jika berhasil, keluaran akan menyebut dua proses dengan nama komputer yang
berbeda. Baru kemudian jalankan benchmark:

```powershell
mpiexec /hosts 2 NAMA_MASTER 1 NAMA_WORKER 1 /wdir "C:\Users\USER\Documents\Codex\Python Matrix Computation" py -3 mpi_benchmark.py --size 250 --seed 7
```

Baris `Komputer proses` pada hasil benchmark harus memuat nama master dan
worker. Checksum juga harus sama dengan benchmark sequential untuk `size` dan
`seed` yang sama.

## Jika proses worker tidak dapat dimulai

Jangan mengubah kode terlebih dahulu. Periksa bahwa:

- nama worker dapat diping dari master;
- MS-MPI dan `mpi4py` sudah dipasang pada kedua komputer;
- path project yang dipakai pada `/wdir` benar dan tersedia di worker;
- Windows meminta atau memblokir izin jaringan/firewall untuk MS-MPI.

MS-MPI mendukung daftar host melalui `/hosts`, dan opsi `/wdir` menentukan
folder kerja proses yang dijalankan. Lihat dokumentasi
[mpiexec Microsoft](https://learn.microsoft.com/en-us/powershell/high-performance-computing/mpiexec?view=hpc19-ps)
untuk parameter tambahan.
