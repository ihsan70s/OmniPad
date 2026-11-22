# Layar PC di HP — WebRTC mirror

PC0.5 • 18 Oktober 2026. Lihat monitor PC di browser HP sambil memakai kontrol yang sudah ada. Ini fitur receiver PC. APK Google TV dan receiver iPad tidak menyediakan mirror ini.

## Mulai

1. Hentikan host PC lama. Gunakan folder PC dari paket terbaru.
2. Jalankan **SETUP_PC.bat** lagi agar aiortc, MSS, Pillow dan dependency video terpasang. Direkomendasikan Python3.11/3.12; instalasi awal membutuhkan internet dan unduhan wheel video.
3. Jalankan **START_PC_MIRROR.bat**. Terminal menyatakan bahwa input LIVE dan screen sharing diizinkan. Belum ada capture hanya karena host berjalan atau HP terhubung.
4. Pindai QR baru pada terminal PC, lalu tekan Hubungkan di HP.
5. Pilih tab **Layar → Mulai layar**. Desktop monitor yang dipilih mulai dibagikan.
6. Tekan **Perbesar** untuk melihat video dan trackpad. Tombol Keyboard & trackpad memindahkan tampilan ke mode Laptop. Dari tab Laptop juga tersedia tombol Layar PC.
7. **Hentikan** menghentikan video tanpa mematikan kontrol PC. Untuk memutus seluruh akses, Ctrl+C pada terminal PC. START_PC.bat biasa tidak mengizinkan mirror.

Tab Layar bukan kamera HP: tidak meminta kamera/mikrofon atau getDisplayMedia pada HP. Siaran video berasal dari capture native pada host PC. Video elemen muted/playsinline; ini memang tanpa audio.

## Kontrol dan alur

Video hanya untuk melihat. Gunakan area trackpad terpisah atau keyboard; mengetuk koordinat pada video belum memindahkan kursor langsung ke posisi absolut. Keyboard/Mouse/Game tetap memakai WebSocket. Gambar bergerak memakai WebRTC, tidak dikirim sebagai screenshot JSON berulang.

Satu koneksi remote terautentikasi aktif boleh membuat satu stream. Tombol Mulai mengirim offer WebRTC lewat WebSocket yang sudah dipasangkan. Host menjawab hanya bila --mirror aktif. Tidak ada endpoint mirror terbuka atau token pada URL media. ID negosiasi menjaga agar jawaban lama tidak dipasang setelah stop/restart.

Stream berhenti pada tombol Hentikan, pindah dari Layar/Laptop ke mode lain, HP masuk background/pagehide, WebSocket berakhir, atau host berhenti. Menutup area Perbesar hanya mengubah layout, bukan otomatis mematikan siaran; status dan tombol Hentikan tetap tersedia.

## Kualitas dan monitor

Default: monitor MSS index1 (layar pertama menurut enumerasi MSS), target15fps, resize mempertahankan rasio maksimal1280×720. Ini batas konfigurasi, bukan hasil performa yang dijamin. Tidak mengklaim gaming60fps/latency tertentu. Teks kecil pada monitor4K bisa memerlukan melihat dari jarak lebih dekat atau menurunkan resolusi desktop.

Untuk bandwidth/CPU lebih ringan, dari terminal di folder PC:

```bat
START_PC_MIRROR.bat --mirror-fps 10 --mirror-width 960
```

Memilih monitor lain:

```bat
START_PC_MIRROR.bat --monitor 2
```

Monitor harus benar-benar tersedia. Tidak ada picker window/monitor pada HP saat ini. Capture mencakup seluruh monitor yang dipilih, termasuk isi yang sedang terbuka. Cursor bergantung dukungan capture OS. Protected content, UAC/login atau secure desktop dapat kosong/tidak tersedia; ini bukan pengganti akses secure desktop.

## Jaringan, izin dan privasi

- HP/PC harus pada LAN pribadi yang saling dapat berkomunikasi. Guest Wi-Fi/client isolation bisa memblokir video walau halaman remote terbuka.
- WebSocket kontrol memakai TCP8765. WebRTC juga memerlukan jalur UDP ICE antara PC dan HP; izinkan aplikasi Python pada firewall profil Private. Jangan mematikan firewall global atau membuka port router.
- Tidak memakai STUN/TURN/cloud relay; hanya host ICE candidate LAN. Bukan remote lewat internet.
- Media WebRTC memakai DTLS/SRTP yang disediakan aiortc/browser. Halaman/pairing HTTP tetap tidak terenkripsi kecuali host dijalankan dengan sertifikat HTTPS/WSS yang dipercaya. Token pairing adalah akses kontrol; tetap gunakan LAN tepercaya.
- Tidak menyimpan capture ke file, merekam video/audio, mengambil clipboard, atau membaca kamera HP. Frame video berada di memori selama encoding/streaming.
- Pada macOS mungkin perlu izin Screen Recording selain izin input. Windows desktop/session harus terbuka. UI memberi pesan bila capture/monitor/negosiasi tidak tersedia.

## Diagnosis

| Kondisi | Langkah |
|---|---|
| Mulai layar nonaktif / mirror belum diaktifkan | SETUP_PC.bat lalu START_PC_MIRROR.bat; pindai QR baru |
| Dependency aiortc/mss tidak ada | Jalankan ulang SETUP_PC.bat pada folder versi terbaru |
| Capture/negosiasi gagal | Pastikan monitor ada, desktop terbuka, dan izin screen recording tersedia jika diminta |
| Remote jalan tetapi video tidak tersambung | Periksa UDP/firewall Private, Wi-Fi guest isolation/VPN dan dukungan WebRTC browser |
| Video tersendat | Coba 10fps/960px; Wi-Fi lebih stabil; periksa CPU PC |
| Browser menolak autoplay | Ketuk permukaan video; muted dan playsinline sudah digunakan |
| Pindah mode lalu video berhenti | Perilaku yang disengaja; tab Layar/Laptop → Mulai layar lagi |

## Bukti pengujian

18 tes backend PASS: input lama, auth, opt-in, tidak capture saat hanya connect, offer invalid, error capture, cleanup disconnect, dan end-to-end WebRTC. Pengujian video memakai gambar sintetis320×180 dan dua peer nyata yang bertukar UDP/DTLS/RTP di loopback; enumerasi interface di-stub ke127.0.0.1 karena runtime membatasi pembacaan interface OS. Frame berhasil dienkode, dikirim dan didekode, lalu stream dihentikan tanpa melepas Ctrl yang masih sengaja ditahan.

DOM suite memakai mocked WebRTC untuk state UI: gating, recvonly video offer, start/answer, video display, docking Laptop, stop dan cleanup. Suite PC/TV/Laptop sebelumnya juga dijalankan sebagai regresi.

**Belum diverifikasi:** capture desktop Windows/macOS nyata, izin OS, encoder/CPU di PC pengguna, sambungan Wi-Fi asli, firewall, browser HP/Safari, rendering/touch, autoplay/fullscreen dan cursor/DRM. Tidak ada klaim physical UAT atau performa jaringan tertentu.

## Sumber teknis

- https://aiortc.readthedocs.io/en/latest/api.html
- https://github.com/aiortc/aiortc/blob/main/examples/server/server.py
- https://python-mss.readthedocs.io/latest/usage.html


## Pilih monitor dan layar penuh
Di tab **Layar**, daftar **Monitor** menampilkan layar yang terdeteksi, resolusi, dan posisi desktopnya. Nomor mengikuti urutan MSS dan bisa berbeda dari nomor Windows Display Settings. Tekan **Muat ulang** setelah memasang/melepas monitor. Pilih monitor sebelum Mulai layar; mengganti pilihan saat siaran aktif akan menyambungkan ulang video. Daftar monitor tidak mengambil gambar desktop.

Tekan **Layar penuh** untuk tampilan video saja. Kontrol keluar dan pilihan monitor tetap tersedia di bagian atas. Proporsi desktop dipertahankan, sehingga layar HP yang berbeda rasio dapat memiliki bidang hitam. Putar HP ke landscape untuk area lebih luas. Jika browser menolak Fullscreen API, video tetap memenuhi halaman browser. **Perbesar** tetap tersedia untuk video bersama trackpad.

Uji otomatis mencakup daftar monitor tanpa capture, pemilihan monitor ke capture, validasi indeks, signaling UI, serta masuk/keluar tampilan penuh. Perangkat fisik multi-monitor Windows dan fullscreen browser HP masih perlu diuji langsung.
