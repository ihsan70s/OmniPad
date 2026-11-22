# Stik game — susunan seperti PS

Mode Game berisi dua analog virtual, D-pad, Segitiga/Lingkaran/Silang/Kotak, L1/L2/R1/R2, Select/Start, serta tombol L3/R3 terpisah. Perbesar stik membuka permukaan kontrol di dalam halaman; ini bukan klaim browser fullscreen/orientation lock. Putar HP ke landscape untuk susunan utama. Portrait memakai reflow vertikal agar tombol tidak diperkecil atau bertumpuk.

| Kontrol | Input PC |
|---|---|
| Analog kiri | W/A/S/D |
| Analog kanan | Panah |
| D-pad | Panah |
| Segitiga | I |
| Lingkaran | L |
| Silang | Spasi |
| Kotak | J |
| L1 / L2 / L3 | Q / Z / Shift |
| R1 / R2 / R3 | E / C / K |
| Select / Start | Tab / Enter |

Konfigurasikan fungsi tombol pada game PC. Analog virtual memiliki threshold arah 0.35 dan diagonal; kecepatan tidak bertingkat. L2/R2 berupa tombol digital, bukan trigger analog. Tidak menyediakan rumble, touchpad PS, lightbar, driver controller atau native gamepad detection.

D-pad dan analog kanan berbagi mapping panah. State source-aware menjaga agar melepas salah satu tidak melepas arah yang masih ditahan kontrol lain. Semua input dibersihkan saat ganti mode, blur, rotate, batal pointer, disconnect, atau Lepaskan tombol.

Dua analog dan banyak tombol serentak tetap bergantung jumlah sentuhan yang didukung HP/browser. Ini belum receiver Android TV/iPad. Live game compatibility dan gesture fisik perlu UAT.
