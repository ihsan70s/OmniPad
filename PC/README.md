# OmniPad — coba di PC sendiri

Paket berisi PRD v2 dan prototipe Python + browser yang bisa dijalankan. Target uji pertama Windows 11. HP/iPad/tablet menjadi controller, PC menjadi receiver. Belum ada installer .exe, true Xbox gamepad, host iPad, screen streaming, atau remote internet.

## Windows: mulai dari sini

1. Ekstrak ZIP. Buka PowerShell di folder `omnipad` yang berisi `server.py`.
2. Instal Python 3.11 atau 3.12 jika belum ada (https://www.python.org/downloads/).
3. Jalankan satu per satu:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe server.py
```

4. PC dan HP harus satu jaringan Wi-Fi pribadi. Buka URL lengkap yang muncul di terminal atau scan QR. Tekan Hubungkan. Akan tertulis DRY RUN: input hanya dihitung, belum mengontrol PC.
5. Jika counter bertambah saat menyentuh trackpad, koneksi berhasil. Tekan Ctrl+C di terminal.
6. Jalankan mode nyata:

```powershell
.\.venv\Scripts\python.exe server.py --live
```

7. Scan QR/URL **baru**. Buka Notepad kosong di PC. Coba gerak mouse, tombol klik, dan kirim teks. Kemudian uji media dan game keyboard.
8. Untuk menghentikan: tombol Lepas semua lalu Ctrl+C pada host. Restart mengganti token akses.

Jika URL salah: jalankan `ipconfig`, pilih IP LAN yang dapat dicapai HP, kemudian:

```powershell
.\.venv\Scripts\python.exe server.py --live --ip 192.168.1.10
```

Ganti IP contoh dengan IP PC sendiri. Izinkan firewall hanya pada profil Private. Jangan membuka router port atau mematikan firewall global. Guest Wi-Fi mungkin memblokir koneksi antar perangkat.

## macOS (eksperimental)

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python server.py
# Setelah dry-run berhasil, hentikan dan jalankan:
.venv/bin/python server.py --live
```

Beri izin Accessibility yang diperlukan pada Terminal/Python melalui pengaturan macOS dan restart host. Media keys dan Unicode harus diverifikasi. Tidak diuji fisik pada paket ini.

## HTTPS opsional

```sh
python server.py --cert cert.pem --key key.pem --ip 192.168.1.10
```

Perangkat pengontrol harus mempercayai sertifikat dan IP/hostname harus cocok dengan SAN. Paket tidak otomatis menerbitkan/memasang sertifikat. HTTP hanya untuk prototipe LAN pribadi yang dipercaya: token dan teks tidak terenkripsi. Jangan gunakan untuk data sensitif. Tautan pairing memberikan akses kontrol sampai host restart.

## Test backend

Dari folder ini:

```sh
python -m unittest discover -s tests -v
```

7 tes lulus saat paket dibuat; test memakai dry-run, tidak membuktikan mouse/keyboard OS atau browser sudah lulus. Ikuti tabel UAT di PRD. Test di Linux headless aman selama tanpa --live.

## Fitur tersedia

- Gerak trackpad, tap kiri, tap dua jari kanan, dua jari scroll.
- Tombol klik kiri/tengah/kanan; tahan tombol kiri + geser trackpad untuk drag.
- Pengiriman teks eksplisit (maksimal 200 karakter), Enter/Backspace.
- Media keys; panah/F/Escape ke jendela PC aktif, bukan universal seek 5 detik.
- Stik susunan PS: dua analog virtual berbasis arah keyboard, D-pad, empat tombol simbol, L1/L2/R1/R2, Select/Start/L3/R3; multi-pointer.
- Satu client aktif, auth token, Origin validation, release saat disconnect dan timeout.

## Keterbatasan

Belum ada automatic reconnect, host approval, per-device revoke, token expiry/sekali pakai, wake lock, PWA install, analog proportional native, XInput, gyro/haptic, executable signed, or installer. Game/anti-cheat bisa mengabaikan simulated input. HTTP tidak aman di jaringan tidak dipercaya. Gesture distance perlu perbaikan sebelum rilis (lihat PRD). Jangan menganggap paket ini produk final siap distribusi.

Isi lengkap requirement, acceptance criteria, release gates, dan langkah implementasi berikutnya ada dalam `PRD_OmniPad_-_Mobile_PC_Controller.md`.


## Pembaruan UI — 17 Oktober 2026

UI memakai skill UX Writing dan Minimalist UI yang diberikan pengguna: latar putih hangat, warna netral, tombol besar, ikon SVG solid, label Indonesia, tab Mouse/Media/Game, bantuan yang bisa dibuka, serta kolom ketik yang disembunyikan sampai diperlukan. Status koneksi dan pesan kesalahan menjelaskan langkah berikutnya. RTT menjadi “Waktu respons koneksi”, DRY RUN menjadi “Mode uji”.

Buka `web/index.html` langsung dari file untuk pratinjau interaktif tanpa mengontrol PC. Saat dijalankan lewat server, tambahkan `?preview=1` untuk mode yang sama. Mode normal tetap memakai WebSocket dan token; kontrol nonaktif sebelum terhubung. Pratinjau bukan koneksi perangkat nyata.

Perbaikan interaksi: gerakan mouse dikirim mengikuti frame, jarak gesture dihitung dari awal agar geseran lambat tidak berubah jadi klik, pointer dibersihkan saat batal/rotasi, serta tombol mendukung keyboard dan multi-pointer. Browser/device fisik tetap membutuhkan UAT.


## Review dan stik lengkap — 17 Oktober 2026

Perbaikan kontras serta skill make-interfaces-feel-better sudah diterapkan di CSS asli project. Tidak ada Tailwind atau halaman Settings dalam sumber yang diberikan. Lihat UI_REVIEW.md untuk temuan, bukti pengujian, dan pemeriksaan yang belum selesai. Lihat GAME_CONTROLLER.md untuk mapping semua tombol dan batasan controller. Tes backend terbaru: 8 PASS.


## Tampilan remote TV minimalis

Halaman awal sekarang membuka mode Media dengan bentuk remote memanjang: tombol arah melingkar, OK di tengah, Kembali/Ketik, volume, putar/jeda, senyap, serta sebelumnya/berikutnya. Tombol daya memutuskan koneksi remote; tidak mematikan PC/TV. Mode Mouse dan stik PS lengkap tetap tersedia melalui tab. Tidak ada klaim dukungan receiver Android TV; output tetap keyboard/media PC.


## Integrasi PC + TV (0.3)

UI sekarang dipakai bersama receiver PC dan TV. Identitas receiver mengatur mode yang tersedia. Windows: SETUP_PC.bat lalu START_PC.bat; TEST_CONNECTION.bat untuk dry-run. Lihat CURRENT_CAPABILITIES.md untuk kemampuan terbaru; PRD/UI review terdahulu adalah baseline historis.


## Mode Laptop (PC0.4)

Buka tab Laptop lalu Layar penuh untuk memakai HP sebagai keyboard dan/atau trackpad PC. Tiga susunan: Keduanya, Keyboard, Trackpad. Baca LAPTOP_MODE.md untuk shortcut, gesture, minimum ukuran keyboard, fullscreen browser dan batasan. Memerlukan host PC terbaru; APK TV tidak berubah.


## Mirror layar PC (PC0.5)

SETUP_PC.bat → START_PC_MIRROR.bat → pindai QR → Layar → Mulai layar. Kirim video WebRTC tanpa suara, target15fps/max1280×720. Mode Laptop bisa menampilkan video yang sama. Normal START_PC.bat tidak mengizinkan capture. Lihat SCREEN_MIRROR.md untuk privacy/izin/firewall/monitor dan hasil tes; desktop Windows serta Wi-Fi perangkat fisik belum diverifikasi.
