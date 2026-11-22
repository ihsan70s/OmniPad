# Keyboard & Trackpad — mode Laptop

Versi PC0.4 — 18 Oktober 2026. Tab **Laptop** membuat HP menjadi perangkat input PC dengan keyboard layar dan/atau trackpad. Google TV tetap hanya mendukung navigasi/media; receiver TV/APK tidak perlu diperbarui untuk fitur PC ini.

## Cara memakai

1. Hentikan host PC versi lama, gunakan folder PC terbaru, lalu jalankan START_PC.bat. Pindai QR baru dari PC dan tekan Hubungkan pada HP.
2. Pilih tab **Laptop**, lalu **Layar penuh**.
3. Pilih **Keduanya**, **Keyboard**, atau **Trackpad**.
4. Landscape memberi ruang lebih luas. Dalam Keduanya, keyboard dan trackpad berdampingan di landscape; portrait memakai susunan vertikal.
5. Tekan **Kembali** untuk keluar dari permukaan penuh. Esc browser/fullscreen juga membersihkan input.

Tombol Layar penuh memperbesar kontrol ke viewport. Bila API fullscreen diizinkan browser, elemen dokumen juga dimasukkan ke fullscreen. Pada browser yang menolak/tidak mendukung, permukaan tetap diperbesar; toolbar browser dapat tetap terlihat. Tidak memaksa orientation lock atau mengklaim aplikasi native.

## Keyboard

QWERTY, angka, simbol dasar, Esc, Tab, Backspace, Enter, Delete, Spasi, panah, F1–F12 opsional. Tombol karakter langsung dikirim sebagai key press/release, bukan batch teks. Label mengikuti susunan QWERTY; hasil karakter mengikuti layout bahasa keyboard pada PC. Beberapa simbol/fungsi berbeda menurut OS/aplikasi.

Ctrl, Alt, Shift dan Win adalah modifier toggle. Contoh Ctrl+C: aktifkan Ctrl, ketuk C, lalu lepas Ctrl atau tekan Lepaskan tombol. Modifier tetap aktif sampai dimatikan; mengganti tab/layout, blur, putus koneksi, keluar fullscreen atau reset akan membersihkannya. Win dipetakan ke key cmd yang merepresentasikan Windows/Meta sesuai OS.

Ini bukan keyboard fisik dengan semua fitur firmware: belum ada numpad, Caps Lock, key-repeat penuh untuk tiap tombol, hardware layout switching, atau secure-attention sequence Windows Ctrl+Alt+Delete. Gunakan ketik teks bawaan HP pada mode Mouse untuk IME/autocorrect/teks panjang; mode Laptop menyediakan keyboard layar sendiri sehingga keyboard native HP tidak menutupi trackpad.

Tombol memiliki minimum44×44 CSSpx. Keyboard lebar minimum648px: di layar sempit geser keyboard secara horizontal atau gunakan landscape/Keyboard saja. Ini menjaga target sentuh dan mencegah tombol dibuat terlalu kecil. Android/iPhone berbeda viewport; perlu UAT fisik.

## Trackpad

Satu area trackpad yang sama digunakan di tab Mouse dan Laptop, sehingga gesture konsisten dan tidak ada handler gerak ganda. Geser satu jari menggerakkan kursor; tap kiri; tap dua jari kanan; dua jari menggulir. Drag: tahan Klik kiri dengan satu jari sambil geser trackpad dengan jari lain. Tombol kiri/tengah/kanan terpisah tersedia.

## Batasan dan verifikasi

Fitur untuk host PC, bukan kontrol iPad/TV. Memerlukan server PC berjalan dan koneksi LAN. Tidak menggantikan perangkat input pada layar login/UAC atau aplikasi/game yang menolak simulated input. Izin Accessibility bisa diperlukan pada macOS; Windows menjadi target utama.

Backend11tests PASS: validasi keyboard/punctuation/modifiers, shortcut ordering, cleanup disconnect, timeout dan autentikasi. DOM laptop suite PASS: gating, tab/relokasi pad, tiga layout, fullscreen fallback dan stub API, Ctrl+C, reset, Fn row, gerak/tap, kembali ke Mouse dan TV gating. Suite DOM PC/TV ikut diuji untuk regresi. Jaringan/Fullscreen pada DOM adalah mock; rendering/touch/fullscreen dan input OS pada HP/PC fisik belum diverifikasi.
