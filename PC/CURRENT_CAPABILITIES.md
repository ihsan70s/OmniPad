# OmniPad — paket PC dan Google TV

Versi PC0.5 / integrasi0.5 • 18 Oktober 2026 • Prototipe LAN untuk diuji pada perangkat sendiri.

Satu antarmuka remote browser HP, dua receiver sesuai perangkat tujuan. APK dipasang pada Google TV; Windows menjalankan host Python. APK Android tidak dapat dipasang langsung pada Windows. HP tidak perlu aplikasi tambahan: buka QR dari perangkat yang ingin dikontrol.

## Isi paket

- `PC/`: host Windows/Python, antarmuka remote, launcher BAT, panduan dan tes backend.
- `TV/OmniPad_Receiver_Android14_Debug.apk`: receiver Google TV v0.2.0-unified.
- `TV/SOURCE/`: source Android lengkap dan Gradle wrapper.
- `QA/`: tes DOM transport PC/TV dan regresi kontrol stik, memakai jsdom sebagai alat uji saja.

## Kemampuan per perangkat

| Fitur | PC Windows | Google TV Android14 |
|---|---|---|
| Media dan volume | Kode tersedia; mengikuti OS/aplikasi | Kode tersedia; mengikuti aplikasi/output audio |
| Tombol arah dan OK | Panah keyboard/Enter | Aksi navigasi aksesibilitas |
| Kembali | Esc pada aplikasi aktif | Android Back |
| Home TV | Tidak ditampilkan | Android Home |
| Mouse/trackpad, klik, gulir, drag | Tersedia | Belum tersedia |
| Ketik teks | Tersedia, ke aplikasi aktif | Belum tersedia |
| Keyboard + trackpad layar penuh (mode Laptop) | Tersedia | Belum tersedia |
| Mirror layar PC ke HP, tanpa audio | Opt-in START_PC_MIRROR.bat + tab Layar | Belum tersedia |
| Stik susunan PS, 2 analog virtual, simbol, L1/L2/R1/R2, Select/Start/L3/R3 | Tersedia sebagai keyboard mapping | Belum tersedia |
| Controller PS/Xbox native, analog proportional, rumble | Belum tersedia | Belum tersedia |
| Kontrol iPad sebagai receiver | Belum tersedia | Tidak berlaku |

Tampilan otomatis menggunakan identitas receiver. Pada TV, tab Mouse/Game dan fitur ketik disembunyikan; Home muncul. Pada PC, lima mode tersedia: Media, Mouse, Game, Laptop dan Layar. Jangan menyebut paket ini produk publik yang sudah memenuhi semua fitur roadmap.

## Mulai di Windows

1. Ekstrak ZIP, buka folder `PC`.
2. Pasang Python3.11/3.12 dari https://www.python.org/downloads/ jika belum ada.
3. Klik dua kali **SETUP_PC.bat**. Perlu internet saat memasang dependency pertama kali.
4. Klik dua kali **START_PC.bat**. Ini mode LIVE: HP pemilik tautan dapat mengontrol PC. Untuk cek koneksi tanpa input OS, buka **TEST_CONNECTION.bat**.
5. Jika firewall Windows meminta izin Python, izinkan hanya pada jaringan Private yang dipakai.
6. Pindai QR terminal menggunakan HP. Pastikan HP dan PC dapat saling menjangkau pada LAN/Wi-Fi pribadi yang sama. Tekan Hubungkan di HP.
7. Uji pertama pada Notepad kosong. Jangan mulai pada kolom password/terminal/transaksi.
8. Tekan Ctrl+C di terminal PC untuk berhenti dan cabut tautan dengan restart host.

Jika QR menunjukkan IP salah, buka terminal pada folder PC dan jalankan `.venv\Scripts\python.exe server.py --live --ip ALAMAT_IP_PC`. Gunakan nilai IPv4 interface LAN aktif dari ipconfig, bukan contoh literal ALAMAT_IP_PC. Hotspot/guest Wi-Fi bisa mengisolasi perangkat. Jangan mematikan firewall global atau membuka port router.

Launcher BAT disediakan tetapi belum dijalankan pada Windows fisik di lingkungan pengembangan. Host PC belum berbentuk installer EXE; perlu Python. macOS melalui instruksi Python di README PC masih eksperimental.

## Mulai di Google TV Android14

1. Pindahkan APK pada folder TV ke TV, misalnya dengan flashdisk.
2. Buka melalui file manager TV. Izinkan pemasangan dari file manager tersebut bila diminta, kemudian instal. Jika versi percobaan lama sudah terpasang, coba update APK ini.
3. Buka **OmniPad Receiver → Aktifkan kontrol**. Baca disclosure dan aktifkan **OmniPad Remote** di pengaturan aksesibilitas TV.
4. Kembali ke receiver, pindai QR di TV dengan HP, lalu tekan **Hubungkan**.
5. Uji arah/OK/Home/Kembali, kemudian aplikasi media. Simpan remote fisik untuk menghentikan receiver jika diperlukan.

Menu bisa berbeda pada firmware Xiaomi. Bila aksesibilitas terhalang Restricted setting, lihat panduan pada README source TV; jangan menganggap izin aktif otomatis. Jika update APK menolak signature, jangan hapus aplikasi lain: catat error; versi debug dengan key berbeda bisa memerlukan uninstall receiver lama dan pairing ulang.

## Mengganti PC dan TV

Buka QR dari perangkat tujuan. Tutup/putuskan sesi sebelumnya jika tidak digunakan. Perubahan tab Mouse/Media/Game adalah perubahan jenis kontrol pada satu receiver, bukan perpindahan perangkat. Tidak ada auto-discovery, daftar perangkat tersimpan, atau penggantian target lewat server cloud pada versi ini.

Tombol daya di HP hanya memutus sesi penggunaan remote pada HP itu; tidak mematikan perangkat atau mencabut token. Untuk TV gunakan **Ganti tautan pairing**/**Hentikan receiver** pada TV. Untuk PC hentikan/restart host agar token berganti.

## Tes dan status

- PC backend: 18 tes PASS, termasuk autentikasi, Origin, sesi eksklusif, reset, timeout dan mapping21key.
- Tes DOM PC: PASS untuk WebSocket, tiga mode, input teks, layout tombol stik, immersive/back, source-aware held keys, reset/disconnect.
- Tes DOM TV: PASS untuk adapter HTTP, sembunyikan fitur PC, Home TV, pairing, mapping9aksi, repeat/cancel arah, error unsupported, disconnect dan penolakan token. Transport jaringan pada tes DOM dimock.
- Android assembleDebug/lintDebug: SUCCESS. Lint 0error/6warning yang tidak disembunyikan (banner vector, saran backup rule dan localization strings).
- APK Signature Scheme v2: verified. MinAPI33, targetAPI34, versionCode2. Debug/test signing.
- Belum diverifikasi: instalasi nyata, rendering/touch HP, izin/live input Windows, lifecycle/accessibility/native HTTP Android pada TV fisik, kompatibilitas aplikasi/game, dan soundbar/CEC. Build dan tes DOM tidak menggantikan UAT perangkat.

Backend: `python -m unittest discover -s tests -v` di folder PC setelah dependency terpasang. Tes DOM opsional: gunakan Node yang kompatibel dengan jsdom, lalu `npm install` dan `npm test` dalam folder QA.

## Batas penggunaan

HTTP LAN tidak mengenkripsi token/teks/perintah. Gunakan jaringan pribadi yang dipercaya; jangan expose internet atau port-forward. QR/token adalah akses kontrol. Tidak ada akun, rekaman layar, pembacaan clipboard, atau log teks ketikan. Receiver TV memakai aksesibilitas untuk global navigation, bukan root/privileged input injection. Semua fitur belum tersedia di seluruh platform.


## Baru: mode Laptop — keyboard dan trackpad layar penuh

Di PC: buka tab Laptop → Layar penuh → pilih Keduanya / Keyboard / Trackpad. Modifier Ctrl/Alt/Shift/Win mendukung shortcut; F1–F12 bisa dibuka. Landscape berdampingan; portrait vertikal. Keyboard dapat digeser mendatar pada layar sempit untuk menjaga area sentuh44px. Fullscreen browser bergantung dukungan/izin; fallback viewport tersedia. Detail dan batasan di PC/LAPTOP_MODE.md. TV APK tidak berubah; mode ini PC-only.


## Baru: lihat layar PC dari HP (PC0.5)

Jalankan ulang SETUP_PC.bat, lalu START_PC_MIRROR.bat. Scan QR → Hubungkan → Layar → Mulai layar. Mode Laptop juga dapat menampilkan video bersama kontrol keyboard/trackpad. Host normal tidak menyiarkan layar. Tanpa suara; target15fps/max1280×720, bukan janji performa. Capture meliputi monitor yang dipilih. Detail izin, jaringan UDP, stop dan batas pengujian ada di PC/SCREEN_MIRROR.md. APK TV tidak berubah.

Uji video lokal memakai frame sintetis dan peer WebRTC nyata di loopback, bukan desktop Windows asli. Enumerasi interface OS di-stub pada pengujian. Jumlah tes backend terbaru18 PASS.


## Pilih monitor dan layar penuh
Di tab **Layar**, daftar **Monitor** menampilkan layar yang terdeteksi, resolusi, dan posisi desktopnya. Nomor mengikuti urutan MSS dan bisa berbeda dari nomor Windows Display Settings. Tekan **Muat ulang** setelah memasang/melepas monitor. Pilih monitor sebelum Mulai layar; mengganti pilihan saat siaran aktif akan menyambungkan ulang video. Daftar monitor tidak mengambil gambar desktop.

Tekan **Layar penuh** untuk tampilan video saja. Kontrol keluar dan pilihan monitor tetap tersedia di bagian atas. Proporsi desktop dipertahankan, sehingga layar HP yang berbeda rasio dapat memiliki bidang hitam. Putar HP ke landscape untuk area lebih luas. Jika browser menolak Fullscreen API, video tetap memenuhi halaman browser. **Perbesar** tetap tersedia untuk video bersama trackpad.

Uji otomatis mencakup daftar monitor tanpa capture, pemilihan monitor ke capture, validasi indeks, signaling UI, serta masuk/keluar tampilan penuh. Perangkat fisik multi-monitor Windows dan fullscreen browser HP masih perlu diuji langsung.
