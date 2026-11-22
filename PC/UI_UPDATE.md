# Pembaruan UI remote

17 Oktober 2026. Berdasarkan ux-writing_SKILL.md dan minimalist-ui_SKILL.md yang diberikan pengguna.

- Putih hangat, charcoal, aksen status pastel, border tipis, tanpa gradient/shadow berat. Font lokal; tanpa CDN.
- Mouse, Media, Game; kontrol 48 px minimum; area sentuh besar; mode ketik dan panduan dibuka saat dibutuhkan.
- Label Indonesia, pesan error dengan langkah berikutnya, mode uji dan pratinjau eksplisit, status koneksi terpisah dari waktu respons.
- Navigasi tab mendukung panah keyboard; tombol held mendukung keyboard dan multi-pointer; reduced motion didukung.
- Gesture movement dihitung dari origin, batching gerak per frame, release lokal pada rotasi/cancel.

## Verifikasi

7 tes backend PASS. JavaScript syntax check PASS. DOM integration memakai jsdom PASS: preview, ketiga tab, teks pratinjau, teks tetap tersimpan, kontrol nonaktif sebelum terhubung, required field, pesan token salah, mode uji, acknowledgment teks, disconnect, tanpa runtime script error pada skenario tersebut. WebSocket pada tes DOM memakai mock; backend diuji terpisah.

Screenshot/layout QA dan gesture perangkat fisik belum diverifikasi: browser headless tidak tersedia dan unduhan browser gagal. Lanjutkan UAT Windows + HP sesuai PRD.

Buka web/index.html langsung untuk pratinjau. Untuk koneksi nyata, jalankan server.py di PC dan buka URL/QR host. Ini tetap remote PC, belum APK Android TV atau receiver iPad.
