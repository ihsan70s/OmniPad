# Contrast revision — 17 October 2026

Computed sRGB palette pair ratios. These are color-pair checks, not a full accessibility or rendered browser audit.

| Pair | Foreground | Background | Ratio | Target |
|---|---|---|---|---|
| Primary text | #20251d | #f7f6f3 | 14.46:1 | 4.5:1 |
| Secondary text | #50564b | #f7f6f3 | 7.01:1 | 4.5:1 |
| Disabled label | #555d4f | #e9ece4 | 5.74:1 | 4.5:1 |
| Button boundary | #7b8472 | #f7f6f3 | 3.61:1 | 3:1 |
| Disabled boundary | #7b8472 | #e9ece4 | 3.26:1 | 3:1 |
| Active tab | #ffffff | #252722 | 15.09:1 | 4.5:1 |
| Trackpad hint | #434e38 | #f0f2e9 | 7.79:1 | 4.5:1 |
| Placeholder | #596150 | #ffffff | 6.46:1 | 4.5:1 |
| Preview badge | #644606 | #fbf3db | 7.83:1 | 4.5:1 |
| Success badge | #28512c | #edf3ec | 8.09:1 | 4.5:1 |
| Error badge | #882927 | #fdebec | 7.63:1 | 4.5:1 |

Removed opacity from disabled trackpad. Disabled controls keep readable labels and remain noninteractive. Selected tab uses charcoal and white, including hover. DOM interaction regression tests PASS. Screenshot unavailable in this revision; no visual QA claim.