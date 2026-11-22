# OmniPad Receiver — Google TV / Android 14

Target pengguna: Xiaomi Google TV, Android TV OS 14. Source mendukung Android 13+ (API33+) karena tombol arah/OK memakai global action AccessibilityService yang tersedia mulai API33.

## Apa yang tersedia

- Aplikasi receiver TV dengan disclosure izin, tombol membuka pengaturan aksesibilitas, QR/URL LAN, ganti tautan, dan hentikan receiver.
- Remote browser HP: arah/OK, Kembali, Home, volume, senyap, putar/jeda, sebelumnya/berikutnya.
- Receiver berjalan dalam lifecycle AccessibilityService yang diaktifkan pengguna; tidak memerlukan root, ADB untuk kontrol, akun cloud, screen capture, atau izin membaca isi jendela.
- Perintah arah berupa aksi diskret, bukan keydown yang tertahan. HP mengulangi arah selama jari ditahan dan berhenti pada pointerup/cancel/blur/hidden.

Mouse, ketik teks lintas aplikasi, PS gamepad, menyalakan TV dari mati, mematikan TV, screen streaming, dan iPad receiver **belum tersedia**. Versi PC tetap terpisah. Remote TV ini tidak memakai kontrak WebSocket PC.

## Instal dan coba

1. Salin `OmniPad_Receiver_Android14_Debug.apk` ke flashdisk atau pindahkan melalui aplikasi transfer file yang Anda gunakan.
2. Di TV, buka APK memakai file manager. Jika diminta, izinkan pemasangan aplikasi dari file manager tersebut, lalu instal.
3. Buka **OmniPad Receiver** dari daftar aplikasi TV.
4. Pilih **Aktifkan kontrol**, baca penjelasan, lalu buka pengaturan aksesibilitas. Aktifkan **OmniPad Remote**.
5. Kembali ke OmniPad Receiver. Hubungkan HP dan TV pada Wi-Fi pribadi yang sama. TV juga boleh memakai kabel LAN ke router yang sama.
6. Pindai QR pada layar TV. Browser HP akan membuka halaman remote dengan kode terisi. Tekan **Hubungkan**.
7. Uji arah/OK di layar Home, lalu buka aplikasi media dan uji putar/jeda. Simpan remote fisik untuk menghentikan receiver bila perlu.

Nama/lokasi menu instalasi dan aksesibilitas bisa berbeda pada firmware Xiaomi. Jika Android menampilkan Restricted setting, periksa App info OmniPad dan opsi Allow restricted settings yang tersedia pada perangkat sebelum mengaktifkan layanan. Jangan mengubah izin aplikasi lain. Jika opsi tidak tersedia di TV, catat pesan/foto menunya; receiver belum boleh dianggap kompatibel.

Tidak ada izin instalasi/pairing yang diaktifkan otomatis. Pengguna mengonfirmasinya di TV.

## Putus dan cabut akses

- Tombol daya pada HP hanya menjeda/memutus penggunaan remote pada HP itu; **tidak mematikan TV dan tidak membatalkan tautan**.
- **Ganti tautan pairing** pada TV membuat token baru; tautan lama gagal untuk permintaan berikutnya. Permintaan yang sudah diproses bisa selesai.
- **Hentikan receiver** menonaktifkan layanan aksesibilitas dan server. Aktifkan lagi melalui Settings untuk sesi baru.
- Reboot/service restart menghasilkan token baru; buka receiver dan pindai ulang QR.

## Prototipe jaringan pribadi

Server HTTP berjalan pada port8765. URL memakai token random192bit di fragment, lalu perintah memakai Authorization header. Origin browser divalidasi; tanpa token benar tidak ada aksi. Command allowlist, body limit1024byte, batas20request/detik dan bounded worker queue membantu membatasi input.

HTTP tidak mengenkripsi token/perintah. Gunakan hanya LAN pribadi yang dipercaya; jangan port-forward atau expose ke internet. Tidak ada persistent trusted-device list, approval terpisah untuk setiap HP, atau TLS dalam prototipe ini. Pemilik tautan dapat mengontrol TV di LAN sampai token diganti/layanan dihentikan. Tidak menyimpan teks input, screenshot, rekaman layar, atau log perintah.

Media keys dikirim ke konsumen media Android. Respons mengikuti aplikasi. Volume bisa dikendalikan soundbar/HDMI-CEC atau fixed-volume mode sehingga perubahan volume sistem belum tentu mengubah volume speaker. Uji pada konfigurasi TV sendiri.

## UAT di TV

| Uji | Expected |
|---|---|
| Buka receiver sebelum izin | Instruksi aktivasi; belum ada QR aktif |
| Aktifkan layanan | Receiver dan QR aktif; URL IP TV benar |
| Scan dari HP, Hubungkan | Terhubung setelah authenticated ping |
| Arah/OK pada Home | Fokus bergerak dan pilihan terbuka |
| Kembali/Home | Aksi sesuai Android; Home kembali launcher |
| Buka YouTube/aplikasi media | Remote masih dapat mengirim aksi saat receiver tidak tampil |
| Volume dan mute | Catat hasil speaker internal vs soundbar |
| Putar/jeda dan next/previous | Catat hasil per aplikasi; tidak semua media mendukung next |
| Token salah / token lama | Ditolak, tidak ada aksi TV |
| Ganti tautan | Permintaan baru dari HP lama ditolak |
| Putus Wi-Fi / background HP | Repeat berhenti; reconnect eksplisit |
| Hentikan receiver | Port ditutup, remote tidak dapat mengontrol |
| Reboot | Pairing ulang jika layanan tersambung lagi; perilaku OEM dicatat |

Belum diuji di perangkat Xiaomi fisik. Build APK dan lint bukan bukti seluruh aksi berfungsi pada firmware pengguna.

## Build source

Gunakan JDK17, Android SDK34/build-tools34, Gradle8.9 dan AGP8.7.3. Buka folder ini di Android Studio, pasang SDK yang diminta, lalu Build APK. Jika wrapper disertakan:

```sh
./gradlew :app:assembleDebug :app:lintDebug
```

Windows memakai `gradlew.bat`. APK output: `app/build/outputs/apk/debug/app-debug.apk`. Paket debug ditandatangani debug key untuk pengujian pribadi; bukan rilis Play Store atau release key jangka panjang.

Third-party: NanoHTTPD2.3.1 (BSD3-Clause), ZXing core3.5.3 (Apache2.0); dependency dan lisensinya ikut dievaluasi sebelum distribusi publik. Build-tool SDK/JDK/Gradle bukan bagian APK source archive kecuali wrapper resmi Gradle.

## Sumber API

- https://developer.android.com/reference/android/accessibilityservice/AccessibilityService
- https://developer.android.com/reference/android/media/AudioManager
- https://developer.android.com/training/tv/get-started/create
- https://developer.android.com/build/releases/agp-8-7-0-release-notes
- https://support.google.com/android/answer/12623953


## Integrasi 0.2.0-unified

UI remote sama dengan versi PC. Pada TV, hanya navigasi/media ditampilkan; Home tersedia, sedangkan tab Mouse/Game dan ketik disembunyikan. Pembaruan ini tetap menggunakan HTTP commands native untuk TV; PC memakai WebSocket. Buka QR PC untuk mengontrol PC.
