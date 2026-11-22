# OmniPad

OmniPad menjadikan HP sebagai remote untuk **PC Windows** atau **Google TV** di jaringan lokal. Jalankan penerima di perangkat tujuan, pindai QR dengan kamera HP, lalu tekan **Hubungkan** di browser. HP tidak memerlukan aplikasi tambahan.

OmniPad masih dalam tahap prototipe. Target utama paket ini adalah Windows dan Google TV dengan Android TV OS 14.

## Unduh dan coba tampilan

1. Di halaman GitHub, pilih **Code → Download ZIP**, lalu ekstrak berkasnya.
2. Buka `Preview.html` dari folder hasil ekstrak untuk mencoba antarmuka tanpa mengirim perintah ke perangkat.
3. Untuk mengontrol perangkat, ikuti panduan Windows atau Google TV di bawah.

## Mengontrol PC Windows

### Instal dan hubungkan

1. Pasang Python 3.11 atau 3.12 jika belum tersedia. [Unduh Python untuk Windows](https://www.python.org/downloads/windows/)
2. Sambungkan HP dan PC ke jaringan pribadi yang sama. PC boleh memakai kabel LAN ke router yang sama.
3. Buka folder `PC/`, lalu klik dua kali `SETUP_PC.bat`. Instalasi dependensi pertama kali memerlukan internet.
4. Klik dua kali `START_PC.bat`. Jika Windows Firewall meminta izin untuk Python, pilih jaringan **Private** yang dipakai.
5. Biarkan jendela terminal terbuka. Pindai QR yang muncul, buka tautan di browser HP, lalu tekan **Hubungkan**. Jika kamera gagal membaca QR, buka URL pairing yang tercetak di terminal.
6. Buka Notepad kosong di PC. Di HP, coba gerakkan kursor dari tab **Mouse**, klik area Notepad, lalu kirim teks pendek.

Untuk mengecek koneksi tanpa mengirim input ke Windows, jalankan `TEST_CONNECTION.bat` sebagai pengganti `START_PC.bat` dan pindai QR dari sesi itu.

### Pilih mode di HP

| Tab | Cara pakai |
| --- | --- |
| **Media** | Gunakan putar/jeda, sebelumnya/berikutnya, volume, dan tombol navigasi. Respons media mengikuti aplikasi yang sedang menangani pemutaran. |
| **Mouse** | Geser satu jari untuk menggerakkan kursor, ketuk untuk klik kiri, ketuk dua jari untuk klik kanan, dan geser dua jari untuk menggulir. Untuk menyeret, tahan tombol **Klik kiri** sambil menggeser trackpad. Gunakan **Ketik teks** untuk mengirim teks ke aplikasi yang sedang aktif. |
| **Game** | Gunakan stik virtual dengan susunan tombol bergaya PlayStation. Windows menerima input sebagai tombol keyboard. Cocokkan pengaturan tombol game dengan [pemetaan OmniPad](PC/GAME_CONTROLLER.md). |
| **Laptop** | Tekan **Layar penuh**, lalu pilih **Keduanya**, **Keyboard**, atau **Trackpad**. Putar HP ke posisi mendatar agar kontrol lebih lega. Lihat [panduan mode Laptop](PC/LAPTOP_MODE.md) untuk tombol pintasan dan gestur. |
| **Layar** | Tampilkan monitor PC di HP dengan mengikuti langkah mirroring di bawah. |

### Tampilkan layar PC di HP

1. Jika host sedang berjalan, tekan **Ctrl+C** di terminal PC. Jalankan ulang `SETUP_PC.bat` jika kamu baru memperbarui paket.
2. Jalankan `START_PC_MIRROR.bat`, pindai QR baru, lalu tekan **Hubungkan**.
3. Buka tab **Layar**, pilih **Monitor**, lalu tekan **Mulai layar**. Gunakan **Muat ulang** jika daftar monitor berubah.
4. Pilih **Layar penuh** untuk memperbesar video atau **Perbesar** untuk menampilkan video bersama trackpad. Mode **Laptop** juga bisa menampilkan video bersama kontrol.
5. Tekan **Hentikan** untuk mengakhiri video sambil tetap terhubung ke PC.

Siaran menampilkan seluruh monitor yang dipilih dan berjalan tanpa audio. Untuk menggerakkan kursor, gunakan trackpad. [Panduan mirroring](PC/SCREEN_MIRROR.md)

## Mengontrol Google TV

1. Salin `TV/OmniPad_Receiver_Android14_Debug.apk` ke TV melalui flashdisk atau aplikasi transfer berkas. [Berkas APK](TV/OmniPad_Receiver_Android14_Debug.apk)
2. Buka APK dari pengelola berkas di TV. Jika diminta, izinkan pengelola berkas tersebut memasang aplikasi, lalu lanjutkan instalasi.
3. Buka **OmniPad Receiver** dari daftar aplikasi TV. Pilih **Aktifkan kontrol**, baca penjelasan, lalu aktifkan **OmniPad Remote** di pengaturan aksesibilitas. Layanan ini menjalankan perintah seperti arah, OK, Kembali, dan Home.
4. Pastikan HP dan TV memakai jaringan pribadi yang sama. Kembali ke OmniPad Receiver, pindai QR yang tampil di TV, lalu tekan **Hubungkan** di browser HP.
5. Uji arah, OK, Kembali, dan Home. Buka aplikasi media untuk mencoba putar/jeda, volume, dan senyap. Respons tombol media bergantung pada aplikasi dan keluaran audio TV.

APK yang disertakan adalah build debug. Menu pemasangan dan aksesibilitas dapat berbeda menurut perangkat. [Panduan receiver Google TV](TV/SOURCE/README.md)

## Berpindah perangkat dan mengakhiri sesi

- Untuk pindah dari PC ke TV atau sebaliknya, putuskan sesi di HP lalu pindai QR dari perangkat tujuan.
- Tombol daya di remote HP memutus sesi di browser. PC atau TV tetap menyala.
- Di PC, tekan **Ctrl+C** di terminal untuk menghentikan host. Jalankan lagi untuk mendapatkan QR baru.
- Di TV, gunakan **Ganti tautan pairing** untuk membatalkan tautan lama, atau **Hentikan receiver** untuk mematikan layanan.

Gunakan jaringan pribadi yang tepercaya dan simpan tautan pairing untuk diri sendiri. Tautan itu memberikan akses kontrol selama masih berlaku. Koneksi LAN memakai HTTP tanpa enkripsi. Hindari membuka port router untuk OmniPad.

## Jika ada kendala

| Gejala | Yang bisa dicoba |
| --- | --- |
| Tautan QR tidak terbuka | Pastikan receiver aktif dan HP bisa menjangkau perangkat di jaringan yang sama. Coba jaringan utama jika perangkat memakai Wi-Fi tamu atau hotspot dengan isolasi antarperangkat. |
| QR di PC menunjukkan IP yang salah | Jalankan `ipconfig`, cari IPv4 adaptor Wi-Fi atau Ethernet yang aktif, lalu jalankan `START_PC.bat --ip ALAMAT_IP_PC` dari folder `PC/` dengan alamat tersebut. |
| Tersambung tetapi PC tidak merespons | Pastikan terminal menjalankan `START_PC.bat` dalam mode LIVE. Fokuskan jendela Notepad, lalu ulangi uji. |
| Tombol **Mulai layar** tidak tersedia | Jalankan `START_PC_MIRROR.bat` dan pindai QR barunya. Jika host gagal memuat dependensi video, jalankan ulang `SETUP_PC.bat`. |
| TV menampilkan **Restricted setting** atau menolak pembaruan APK | Cek opsi pemasangan dan aksesibilitas dari panduan receiver. APK percobaan lama dapat memakai kunci penandatanganan yang berbeda. [Panduan receiver Google TV](TV/SOURCE/README.md) |

## Kode sumber dan pengujian

| Lokasi | Isi |
| --- | --- |
| [PC/](PC/) | Host Python, antarmuka browser, launcher Windows, dan tes backend. |
| [TV/SOURCE/](TV/SOURCE/) | Kode penerima Android dan Gradle wrapper. |
| [QA/](QA/) | Tes antarmuka PC, TV, Laptop, dan mirroring dengan jsdom. |
| [Preview.html](Preview.html) | Pratinjau antarmuka yang dapat dibuka langsung di browser. |

Jalankan tes backend di folder `PC/` setelah setup.

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Jalankan tes antarmuka di folder `QA/` dengan Node.js yang kompatibel dengan jsdom.

```powershell
npm install
npm test
```

Paket mencatat pengujian backend dan antarmuka otomatis serta build APK debug. Instalasi pada TV fisik, input Windows dari HP, gestur di browser HP, dan kompatibilitas aplikasi atau game masih memerlukan uji perangkat. [Panduan host PC](PC/README.md) · [Catatan build Android](TV/SOURCE/BUILD_STATUS.md)
