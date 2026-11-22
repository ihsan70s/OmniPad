# OmniPad — PRD dan spesifikasi implementasi

Versi 2.0 • 16 Oktober 2026 • Bahasa: Indonesia

**Status:** spesifikasi baseline dan prototipe runnable tersedia. Belum berstatus produk final atau lolos UAT perangkat fisik. Tanda fase selesai dalam draft awal tidak dipertahankan karena tidak disertai bukti implementasi.

## 1. Tujuan dan keputusan produk

OmniPad mengubah browser HP, iPad, atau tablet menjadi pengontrol mouse, input teks, remote media, dan tombol permainan untuk komputer di jaringan lokal. Host desktop menjalankan server dan menerjemahkan input ke sistem operasi. Browser saja tidak dapat menggerakkan kursor komputer lain tanpa host atau perangkat HID.

Target rilis pertama: satu pengontrol untuk satu PC Windows 11 dalam satu sesi pengguna desktop yang sedang terbuka. Windows 10 dan macOS harus diverifikasi tersendiri; macOS memerlukan izin sistem yang sesuai. Linux belum menjadi target support.

**Dua makna tablet:** (1) tablet sebagai pengontrol PC masuk cakupan browser; (2) HP mengontrol seluruh iPad/tablet sebagai perangkat tujuan tidak termasuk MVP. Jangan menjanjikan host Python identik berjalan di iPadOS. Opsi masa depan: integrasi per aplikasi, native platform, atau perangkat HID; masing-masing membutuhkan feasibility spike. Android target juga memerlukan kajian izin dan distribusi aplikasi terpisah.

Keputusan ini merupakan asumsi baseline agar pengembangan dapat berjalan, bukan keputusan bisnis yang sudah dikonfirmasi pengguna.

## 2. Pengguna, masalah, hasil

| Persona | Kebutuhan | Hasil yang dinilai |
|---|---|---|
| Menonton dari sofa | Putar/jeda, volume, navigasi | Tidak perlu mengambil mouse untuk kontrol dasar |
| Presenter | Berpindah slide, escape | Input menuju aplikasi presentasi yang aktif |
| Mouse cadangan | Gerak, klik, scroll, drag, ketik | Dapat mengisi kolom pencarian dan membuka hasil |
| Pemain kasual | Menahan arah dan aksi bersamaan | Game yang menerima keyboard dapat dimainkan |

Keberhasilan MVP: pengguna baru dapat mengikuti panduan sampai terhubung dalam ≤3 menit setelah dependency host terpasang; alur mouse/teks/media utama lulus UAT; tidak ada tombol tertahan setelah disconnect yang terdeteksi host. Waktu instalasi Python dan dependency dicatat terpisah.

## 3. Batas cakupan dan prioritas

| ID | Requirement | Prioritas rilis | Status paket ini |
|---|---|---|---|
| FR01 | URL LAN dan QR host | P0 | Kode tersedia; QR bila qrcode terpasang |
| FR02 | Autentikasi token acak per startup | P0 | Kode tersedia |
| FR03 | Satu sesi pengontrol aktif | P0 | Kode dan tes tersedia |
| FR04 | Gerak relatif satu jari; tap kiri; tap dua jari kanan | P0 | Kode tersedia; gesture perlu UAT |
| FR05 | Scroll dua jari; tombol kiri/tengah/kanan | P0 | Kode tersedia; perlu kalibrasi |
| FR06 | Tahan tombol mouse untuk drag sambil geser trackpad | P0 | Kode tersedia |
| FR07 | Media play/pause, previous/next, volume, mute | P0 | Kode tersedia; backend/app perlu UAT |
| FR08 | Panah kiri/kanan, F, Escape untuk aplikasi aktif | P0 | Kode tersedia; hasil bergantung aplikasi |
| FR09 | Input teks eksplisit dengan tombol kirim | P0 | Kode tersedia; Unicode perlu UAT |
| FR10 | Gamepad keyboard WASD, Space, Enter, Esc | P0 | Kode tersedia; bukan XInput |
| FR11 | Release all, disconnect cleanup, watchdog | P0 | Kode dan tes tersedia |
| FR12 | Status live/dry-run, RTT, jumlah event | P0 | Kode tersedia |
| FR13 | Host approval, revoke per perangkat, pairing token sekali pakai | P1, wajib sebelum distribusi luas | Spesifikasi; belum dibuat |
| FR14 | Profil shortcut, sensitivitas, natural scroll | P1 | Spesifikasi; belum dibuat |
| FR15 | Wake lock, fullscreen opsional, PWA HTTPS | P1 | Spesifikasi; belum dibuat |
| FR16 | Analog 360°, ABXY, shoulder buttons, XInput | P2 | Feasibility dan driver belum selesai |
| FR17 | Gyro, haptic, multi-player/controller slots | P2 | Belum dibuat |
| FR18 | Host GUI, executable signed, auto update | P1/rilis publik | Belum dibuat |

Tidak termasuk: screen streaming, kontrol jarak jauh internet, port forwarding, login akun cloud, transfer file, clipboard reading, keylogging, kontrol layar login/UAC, sleep/shutdown remote, arbitrary command execution. Sleep/shutdown dihapus dari P0 karena tidak membantu pengujian inti dan memerlukan konfirmasi/otorisasi khusus.

## 4. Matriks platform

| Peran | Platform | Dukungan baseline |
|---|---|---|
| Pengontrol | Android Chrome | Browser foreground; uji touch dan keyboard |
| Pengontrol | iPhone Safari | Browser foreground; jangan bergantung vibration/fullscreen |
| Pengontrol | iPad Safari / tablet Android | Layout responsif; uji portrait dan landscape |
| Host | Windows 11 x64 desktop | Target uji pertama; Python + pynput |
| Host | macOS | Eksperimental; izin Accessibility dan verifikasi media keys |
| Host | iPadOS / Android | Tidak didukung host paket ini |

HTTP LAN merupakan jalur prototipe di jaringan pribadi yang dipercaya. Token dan teks melewati jaringan tanpa enkripsi. Jangan membuka port router, mengakses lewat Wi-Fi publik, atau menganggap token menggantikan TLS. Untuk rilis publik: sertifikat dipercaya perangkat, HTTPS/WSS, pairing approval, threat review, dependency lock, dan packaging menjadi release gates.

## 5. Alur end-to-end

1. Pengguna memasang Python 3.11/3.12 di PC; membuat virtual environment; memasang requirements.
2. Jalankan dry-run. Host menampilkan IP, port 8765, tautan dengan token di URL fragment, serta QR bila tersedia.
3. HP dan PC berada pada jaringan yang dapat saling menjangkau. Guest Wi-Fi/client isolation dapat menggagalkan koneksi walau SSID sama.
4. Scan QR atau buka URL lengkap. Pengguna menekan Hubungkan; token dikirim sebagai pesan pertama WebSocket, tidak di query string. Fragment dihapus dari address bar halaman setelah dibaca; tautan awal masih merupakan rahasia akses.
5. Host memvalidasi Origin, token, batas koneksi dan satu sesi aktif. Tanpa token benar tidak ada input dieksekusi.
6. Client menampilkan mode DRY RUN atau LIVE dan RTT. Mode Mouse menjadi default.
7. Pengguna memilih tab; host melepas semua input saat perpindahan mode melalui event release.
8. Saat blur/hidden, client meminta release; saat hidden client menutup koneksi. Host akhirnya melepas tombol lewat cleanup/timeout walau event browser gagal terkirim.
9. Putus koneksi: kontrol dinonaktifkan, halaman menampilkan tombol hubungkan ulang. Tidak ada replay input setelah reconnect.
10. Ctrl+C atau menutup terminal menghentikan host. Restart menghasilkan token baru dan mencabut tautan lama.

Flow pengujian: dry-run → validasi event diterima → stop host → start --live → buka Notepad di PC → uji teks dan mouse → buka media → uji remote → game keyboard → disconnect safety.

## 6. Spesifikasi UI/UX

Gunakan page responsive untuk permukaan kontrol utama: ruang gesture dan multi-touch lebih cocok daripada modal. Dialog kelak hanya untuk persetujuan pairing di host, penggantian sesi, dan aksi berisiko. Ini proyek mandiri, tidak diasumsikan menggunakan UI KIT Herca.

### 6.1 Halaman kontrol

Header: OmniPad, status koneksi, label LIVE/DRY RUN, RTT, tombol Lepas semua. Navigasi: Trackpad, Remote, Gamepad. Minimal target sentuh 48×48 CSS px; kontras teks WCAG AA ditargetkan dan harus diaudit sebelum rilis. Ikon wajib memiliki label. Hindari perubahan layout saat tombol ditekan. Fokus keyboard harus terlihat. Jangan menyampaikan status hanya dengan warna.

Trackpad: area sentuh ≥210 px tinggi; hint gesture; tombol mouse terpisah; textarea berlabel; Kirim teks; Enter; Backspace. Keyboard native muncul lewat textarea, bukan simulasi global key event browser. Nilai teks tidak dikirim setiap keystroke agar IME/autocorrect tidak menggandakan input. Setelah kirim, field dikosongkan; ack saat ini menandakan adapter menerima perintah, bukan aplikasi tujuan menerima teks.

Remote: kontrol media terpisah dari shortcut aplikasi. Tampilkan “Panah dan F dikirim ke jendela aktif; hasil bergantung aplikasi.” Jangan memberi label “+5 detik” untuk panah generik. Seek 5 detik membutuhkan profil aplikasi yang telah diuji.

Gamepad MVP: WASD dan Space/Enter/Esc, tombol multi-pointer independen. Caption “Keyboard mapping — bukan Xbox controller.” Landscape disarankan, tidak dipaksa; orientation lock/fullscreen bergantung izin dan browser. Versi analog kelak membutuhkan vector normalized, deadzone 0,15 sebagai nilai awal, dan neutral state saat pointer hilang.

### 6.2 Field dan validasi

| Field | Required | Batas | Error |
|---|---|---|---|
| Token | Ya sebelum connect | Token dari host; jangan simpan localStorage | Masukkan token dari PC |
| Teks | Ya saat Kirim teks | 1–200 karakter; tolak kontrol selain newline/tab | Teks harus 1–200 karakter |
| IP host CLI | Opsional | Alamat interface PC yang dapat dicapai HP | Gunakan --ip sesuai ipconfig |
| Port CLI | Ya/default | 1–65535; default 8765 | Port sedang dipakai atau tidak valid |
| Sertifikat dan private key | Keduanya bila TLS | File PEM cocok; cert dipercaya pengontrol | Sertifikat/key gagal dimuat |

### 6.3 State dan copy

| Kondisi | Copy/aksi |
|---|---|
| Idle | Belum terhubung · Hubungkan |
| Connecting | Menghubungkan… |
| Dry-run ready | Terhubung · DRY RUN (tanpa kontrol PC) |
| Live ready | Terhubung · LIVE |
| Wrong token | Koneksi ditolak: unauthorized · scan tautan host terbaru |
| Busy | Koneksi ditolak: busy · akhiri sesi sebelumnya |
| Disconnected | Terputus. Hubungkan ulang secara manual. |
| Backend error | input_backend_failed · cek izin dan restart host |
| Timeout | invalid_or_timed_out · koneksi ditutup dan input dilepas |
| Jaringan gagal | Gagal terhubung. Cek IP, Wi-Fi, firewall, dan server. |

Prototipe masih menampilkan kode error teknis. Sebelum rilis publik, petakan ke pesan Indonesia kontekstual dan pisahkan timeout/invalid payload secara eksplisit.

## 7. Aturan gesture dan input

- Pergerakan mouse relatif; default multiplier 1,5. Delta per event dibatasi ±500. Tidak ada koordinat absolut atau screenshot.
- Tap <250 ms dengan perpindahan kecil menghasilkan satu click. Implementasi prototipe memakai deteksi movement per event; sebelum rilis perbaiki menjadi akumulasi jarak dari titik awal agar slow drag tidak salah klik.
- Dua pointer menghasilkan scroll; setelah salah satu diangkat jangan mengubah sisa gesture menjadi gerak mouse. Tap dua jari menghasilkan right click.
- Drag eksplisit: tahan tombol kiri dengan satu jari dan gerakkan jari lain di trackpad. Release tombol menghentikan drag.
- Pointer capture wajib; pointercancel/lostpointercapture melepas tombol. Mode change/blur/disconnect memanggil release-all.
- Keydown berulang untuk key yang masih held bersifat idempotent. Keyup untuk key yang tidak held diabaikan. Keyboard mapping tidak menjamin keyboard autorepeat atau dukungan game/anti-cheat.
- Text dikirim ke aplikasi yang fokus di PC. Tidak ada pemilihan target aplikasi otomatis. Jangan tes awal pada terminal, password, transaksi, atau form yang berisiko; gunakan editor teks kosong.
- Semua perintah input tunduk token valid dan exclusive session; client tidak boleh memilih shell command, file path, atau kode executable.

## 8. Arsitektur dan dependency

Browser HTML/CSS/Vanilla JS → WebSocket native → aiohttp Python → Input adapter → pynput → desktop OS.

Pilih aiohttp tunggal untuk HTTP + WebSocket agar tidak mencampur Socket.IO dengan WebSocket native. Flask-SocketIO/eventlet tidak diperlukan untuk MVP ini. Payload Socket.IO tidak kompatibel langsung dengan native WebSocket.

File: server.py (HTTP/auth/session/adapter), web/index.html (UI dan event), tests/test_host.py (validation dan integration), requirements.txt, README.md. Aset lokal tanpa CDN agar sesi berjalan tanpa internet setelah dependency terpasang. Server tidak membuka endpoint file lain.

Dependency menggunakan rentang versi kompatibel; ini **bukan reproducible lockfile**. Sebelum release, instal pada PC target, audit, pin versi hasil verifikasi, simpan lock dan daftar lisensi. Python runtime dan installer final belum dipaketkan.

Input OS melalui pynput di thread event loop cocok untuk prototipe kecil; pengiriman text/adapter lambat berpotensi memblokir. Sebelum release, pindahkan adapter ke dedicated serial worker dengan bounded queue: preserve urutan down/up/release, coalesce move, drop stale move, prioritaskan reset. Jangan menjalankan beberapa worker input tanpa ordering.

## 9. Kontrak protokol v1 yang diimplementasikan

Endpoint GET / mengirim UI, GET /ws melakukan upgrade. Origin harus persis scheme://host:port yang sedang diakses. Client harus mengirim auth dalam ≤5 detik. Max frame 4096 byte; maksimal 240 pesan/detik per session; 10 percobaan upgrade/menit per IP; maksimum delapan socket bersamaan termasuk pra-auth. Rate limit bukan perlindungan DDoS penuh; tabel attempts perlu eviction untuk rilis.

```json
{"token":"token-dari-fragment"}
{"type":"ready","dry_run":true,"protocol":1}
{"type":"move","dx":12.5,"dy":-4}
{"type":"scroll","dy":1}
{"type":"button","name":"left","down":true}
{"type":"button","name":"left","down":false}
{"type":"key","name":"w","down":true}
{"type":"key","name":"w","down":false}
{"type":"text","text":"Halo OmniPad"}
{"type":"release"}
{"type":"ping","id":123}
{"type":"pong","id":123}
{"type":"ack","events":8}
{"error":"unauthorized"}
```

Per baris adalah pesan terpisah. move dx/dy finite numeric ±500, scroll dy finite ±20, down harus boolean; nama key/button allowlist di server. Text 1–200 karakter. Float gerak dibulatkan oleh adapter saat live; fractional accumulation perlu ditambahkan jika gerakan lambat terasa terpotong.

WebSocket menjaga urutan dalam koneksi. Prototipe belum memakai sequence/session ID atau resumable command. Reconnect selalu sesi baru dan tidak mengirim ulang input lama. Versi berikutnya menambahkan seq monoton, request_id untuk aksi diskret, session_id, error detail dan ack per request. Unknown type menutup koneksi; input held dilepas.

Client mengirim ping aplikasi tiap 500 ms; server timeout receive 3 detik. Protocol ping/pong tambahan oleh aiohttp bukan pengganti heartbeat aplikasi. Timeout dihitung sejak pesan aplikasi terakhir; target safety ≤3,5 detik pada event loop sehat, bukan garansi ketika OS/proses membeku. Host watchdog background/native diperlukan jika ingin jaminan lebih kuat.

## 10. Security dan privasi

Model ancaman: orang lain di LAN mencoba mengambil kontrol; halaman asing menghubungkan WebSocket; token bocor; payload invalid; tombol tertahan; rate flood. Kontrol tersedia: token random 24 byte entropy sebelum encoding, compare_digest, exact Origin check, allowlist, schema validation, limit pesan/koneksi, single active client, release cleanup, token baru saat restart, tidak ada shell endpoint.

Origin bukan pengganti autentikasi dan dapat dipalsukan client non-browser. HTTP tidak melindungi token dari penyadapan/MITM. Tautan QR grants control, token berlaku hingga host restart dan dapat dipakai kembali setelah disconnect. Jangan menyebutnya token sekali pakai atau pairing approval.

Tidak menyimpan teks ketikan, riwayat input, screenshot, atau credentials. stdout menampilkan pairing URL agar dapat dipindai; perlakukan terminal/screenshot QR sebagai informasi rahasia. Access log dinonaktifkan. Runtime event counter tidak mencatat isi teks. Perangkat yang sudah tahu token tidak dapat dicabut satu per satu dalam MVP; stop/restart host mencabut semua.

Release publik wajib: TLS dengan sertifikat dipercaya, local host approval + one-time expiring pairing, per-device revocation/session lifecycle, host panic control independen jaringan, log audit tanpa teks/token, bounded memory, dependency patch policy. Tidak menjalankan host sebagai administrator kecuali analisis spesifik membuktikan perlu; elevated app dan UAC tidak didukung.

## 11. Kebutuhan nonfungsional dan metrik

| Area | Target penerimaan | Cara ukur |
|---|---|---|
| Network RTT | p95 ≤50 ms pada Wi-Fi sehat yang dicatat | ≥1.000 ping, warmup 10 detik; median/p95/p99 |
| Input-to-visible | Target p95 ≤100 ms, diukur terpisah | Rekam sentuhan dan layar PC high-frame-rate; minimal 100 aksi |
| Safety | Release ≤3,5 detik setelah app messages berhenti pada proses sehat | Simulasikan disconnect dan stall client |
| Stability | 30 menit tanpa crash, stuck key, atau antrean membesar | Sesi campuran + monitor memori |
| Multi-touch | Empat pointer serentak pada device yang mendukung | Dua arah/aksi + tombol; pointercancel dan rotasi |
| Responsiveness | 360–1366 CSS px, portrait/landscape | Safari/Chrome physical device |
| Privacy | Tidak ada token/teks dalam persistent log | Review stdout/access log/data files |

RTT bukan input latency dan bukan bukti mencapai <16 ms. Paket belum mencatat distribusi RTT otomatis; label browser saat ini hanya sample terakhir. Buat diagnostic collector sebelum menilai target numerik. Bandingkan Wi-Fi 2,4/5 GHz, hotspot, guest isolation, interferensi, dan PC Ethernet sebagai kondisi uji, bukan garansi performa.

## 12. Acceptance criteria

| ID | Given / When / Then | Bukti |
|---|---|---|
| AC01 | Host berjalan; URL benar; token benar → ready dan mode ditampilkan | Integration + device |
| AC02 | Token salah → tidak ada event OS dan unauthorized | Integration |
| AC03 | Origin asing → handshake ditolak 403 | Integration |
| AC04 | Client A aktif; B connect → B busy dan A tetap aktif | Integration |
| AC05 | Mouse mode; geser → kursor bergerak sesuai arah | Windows UAT |
| AC06 | Tap satu/dua jari → satu left/right click tanpa double trigger | Device UAT |
| AC07 | Scroll dua jari → dokumen scroll; tidak pindah kursor saat jari terangkat | Device UAT |
| AC08 | Tahan kiri dan geser → drag; release → drop | Windows UAT |
| AC09 | Editor fokus; kirim teks Indonesia → isi sesuai tanpa duplikasi IME | Windows UAT |
| AC10 | Media player aktif; media buttons → hasil sesuai mapping OS/player | App matrix |
| AC11 | Game keyboard; tahan W + Space → dua key held; lepas satu tidak melepas lainnya | Device/game UAT |
| AC12 | Key held; disconnect → held kosong; tidak replay ketika reconnect | Integration + OS UAT |
| AC13 | Key held; client berhenti mengirim pesan → cleanup setelah timeout | Integration + OS UAT |
| AC14 | NaN, unknown key/type, oversize text → ditolak dan input dilepas | Validation/integration |
| AC15 | Host dry-run → event counter naik, tidak ada panggilan OS | Adapter/test + UAT |
| AC16 | Ganti tab/blur/rotasi/cancel → tidak ada stuck key | Device UAT |
| AC17 | Host restart → token lama gagal, token baru sukses | Manual/integration extension |
| AC18 | Pointer movement lambat/tap bergerak → tidak salah klik | Release gate gesture fix |
| AC19 | Flood >240/s atau >4096 bytes → koneksi dihentikan tanpa stuck input | Tambah load integration sebelum release |
| AC20 | 30 menit penggunaan → memori stabil dan safety tetap bekerja | Soak UAT |

## 13. Rencana pengujian sampai hasil dapat dicoba

### 13.1 Otomatis (telah dijalankan di lingkungan pengembangan)

Perintah `python -m unittest discover -s tests -v` dari folder omnipad. Hasil saat paket dibuat: **7 tests PASS** untuk validation rejection, release idempotence, token salah, origin asing, exclusive session/disconnect release, invalid payload release, watchdog timeout. Menggunakan dry-run adapter sehingga tidak membuktikan input OS, gesture, browser rendering, atau media/game compatibility.

### 13.2 UAT fisik berurutan

| Langkah | Aksi | Hasil yang diharapkan |
|---|---|---|
| 1 | Jalankan default; scan dan hubungkan | DRY RUN, bukan LIVE |
| 2 | Geser/klik/ketik | Counter naik; PC belum berubah |
| 3 | Buka URL dari HP lain | busy selama HP pertama aktif |
| 4 | Stop lalu jalankan --live | Terminal LIVE; gunakan URL token baru |
| 5 | Fokus Notepad kosong; geser dan klik | Kursor/klik bekerja |
| 6 | Ketik “Tes OmniPad 123”; Kirim teks | Satu teks yang sama tampil |
| 7 | Uji kanan/tengah/dua-jari scroll/drag | Aksi tepat dan tidak tertahan |
| 8 | Buka pemutar media; uji setiap tombol | Catat aplikasi, hasil, dan unsupported keys |
| 9 | Buka game yang menerima keyboard | WASD dan aksi bersamaan bekerja |
| 10 | Tahan W; matikan Wi-Fi HP | W dilepas setelah disconnect/timeout terdeteksi |
| 11 | Background browser, rotasi, pindah tab | Input dilepas; reconnect eksplisit |
| 12 | Jalankan 30 menit; catat RTT dan error | Tidak ada crash/stuck input |

Catatan hasil: tanggal, host OS/build, Python/dependency versions, browser/device/OS, jaringan, live/dry-run, AC ID, expected, actual, pass/fail, bukti, severity. Jangan masukkan pairing token atau teks pribadi dalam bukti.

Definisi selesai MVP untuk penggunaan pribadi: seluruh AC01–AC17 relevan lulus pada kombinasi host/client yang diumumkan, bug gesture AC18 diperbaiki, soak lulus, dan keterbatasan diumumkan. Produk publik juga wajib menyelesaikan security gates, AC19–20, installer, TLS, approval dan accessibility audit. Paket ini belum memenuhi definisi produk publik selesai.

## 14. Backlog implementasi dan dependensi

| Urutan | Pekerjaan | Dependensi | Exit criterion |
|---|---|---|---|
| 0 | Konfirmasi OS PC, HP, arti target tablet | Pemilik produk | Matriks target disepakati |
| 1 | Host, native WebSocket, auth, dry-run, allowlist | Python | Tes backend lulus; tersedia di paket |
| 2 | Client trackpad/remote/keyboard/game keys | Host | Browser dan device UAT; kode dasar tersedia |
| 3 | Perbaiki gesture distance, fractional mouse, worker queue, rate tests | UAT awal | AC18–19 + backlog reliability selesai |
| 4 | Windows physical UAT + media matrix | Host Windows | AC05–13 dan soak lulus |
| 5 | Host approval, expiring one-time pairing, TLS, revoke | Security design | Unauthorized LAN tests dan trusted-device flow lulus |
| 6 | GUI tray, installer, signed executable, lock deps | Stable host | Fresh PC install/uninstall lulus |
| 7 | macOS port + permission onboarding | Mac fisik | Matriks dukungan eksplisit |
| 8 | True virtual gamepad feasibility | Driver maintained + security review | Game mengenali controller, neutral/reset lulus |
| 9 | Tablet receiver feasibility | Per platform native/HID research | Proof of concept atau keputusan tidak didukung |

Tidak memberi estimasi kalender pasti sebelum OS/device dan hasil uji diketahui. Untuk dikerjakan AI coding agent: kerjakan urutan 1–4 dulu, jalankan tests tiap perubahan backend, jangan menandai OS UAT lulus tanpa perangkat. Jangan mengganti keyboard mapping menjadi klaim XInput.

## 15. Virtual gamepad dan fitur lanjutan

ViGEmBus berstatus end-of-life menurut maintainer; jangan menjadikannya dependency default baru. True XInput memerlukan driver virtual yang sesuai dan dievaluasi pemeliharaan, signing, lisensi, install/uninstall, kompatibilitas Windows/game/anti-cheat, dan keamanan supply chain. Python vgamepad saja bukan pengganti driver. Keputusan driver ditunda sampai feasibility selesai.

Analog, L2/R2, ABXY membutuhkan state snapshot controller dan heartbeat neutralization. Keyboard emulation tidak menyediakan analog proportional, rumble feedback atau player-2 terpisah. Dua HP yang mengirim WASD berbagi keyboard sistem, bukan dua controller.

Wake lock membutuhkan secure context dan dapat dicabut; UI harus fallback “Atur layar tetap menyala secara manual”. Fullscreen/orientation lock hanya setelah user gesture dan failure tidak boleh memblokir kontrol. Vibration/gyro hanya progressive enhancement, dengan permission dan feature detection. PWA install/offline tidak dianggap tersedia pada HTTP LAN; offline UI tidak sama dengan input host offline.

## 16. Troubleshooting dan operasi

- Halaman tidak terbuka: host masih berjalan? IP benar? gunakan `ipconfig` (Windows), pilih interface Wi-Fi/LAN yang digunakan, bukan VPN/Docker. Jalankan `python server.py --ip 192.168.x.x`.
- Firewall: izinkan Python/port 8765 inbound hanya profil jaringan Private; jangan mematikan firewall global. Hotspot/client isolation dapat memblokir peer traffic.
- Address already in use: hentikan host sebelumnya atau `--port 8766`; gunakan URL baru dengan port baru.
- Terhubung tetapi tidak menggerakkan PC: periksa DRY RUN; restart dengan --live; pastikan pengguna desktop aktif dan izin OS. Pynput gagal import pada headless server adalah wajar untuk live input.
- Media keys tidak merespons: uji aplikasi lain; pastikan media session; panah/F bukan shortcut universal. Catat hasil, jangan klaim semua aplikasi didukung.
- Unicode tidak sesuai: uji layout keyboard dan IME; future adapter paste harus meminta persetujuan dan memulihkan clipboard bila digunakan. Paket ini tidak membaca clipboard.
- Input macet: tekan Lepas semua, tutup browser, lalu Ctrl+C host. Jika proses hang, hentikan proses dari PC; safety proses yang mati paksa perlu diuji OS.
- Sertifikat: --cert dan --key mengaktifkan HTTPS, tetapi tidak otomatis membuat sertifikat dipercaya HP. Provisioning sertifikat tepercaya merupakan pekerjaan terpisah.

## 17. Sumber teknis dan dasar perubahan

Diperiksa 16 Oktober 2026. Referensi menjelaskan batas API, bukan bukti implementasi paket telah lulus device UAT.

1. aiohttp WebSocket server: https://docs.aiohttp.org/en/stable/web_reference.html#aiohttp.web.WebSocketResponse
2. pynput platform limitations: https://pynput.readthedocs.io/en/latest/limitations.html
3. Screen Wake Lock secure context: https://developer.mozilla.org/en-US/docs/Web/API/WakeLock
4. ViGEm end-of-life: https://docs.nefarius.at/projects/ViGEm/End-of-Life/
5. Apple sandbox background: https://developer.apple.com/documentation/security/protecting-user-data-with-app-sandbox — konteks pembatasan platform; bukan bukti bahwa host Python ini mendukung iPadOS. Feasibility receiver iPad tetap belum selesai.

## 18. Keputusan yang masih membutuhkan data nyata

OS dan versi PC pengguna; browser HP/tablet; perangkat yang dimaksud sebagai receiver; daftar media player/game; apakah penggunaan hanya pribadi atau distribusi; kebutuhan HTTPS sejak uji pertama; apakah teks Unicode/IME menjadi blocker. Default paket: Windows-first, penggunaan pribadi LAN, tablet sebagai controller, keyboard-mapped gamepad, HTTP dry-run sebelum live. Jika asumsi ini berubah, scope dan acceptance matrix harus diperbarui.
