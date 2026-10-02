# kernel-patches — maintained out-of-tree ports (reference + Samsung 5.4 adaptation)

These ship on `main` so CI float steps can fetch them from `origin/main`.
Nothing here is applied by default; each is gated behind its own
`workflow_dispatch` opt-in flag.

## ntsync/
- `ntsync_base.patch` — upstream NTSync base (WildKernel `kernel_patches`
  TIP `41ae18b3`, file `common/ntsync/ntsync_base.patch`), unmodified.
- `samsung-ntsync-compat.patch` — Samsung 5.4 compat layer (vendor-style
  lockdep rewrite; base Kconfig/Makefile hunks kept as-is).
- Verified: base + compat both `git apply --check` CLEAN on `79184eab5`.
- Planned inputs: `use_ntsync` + `pin_ntsync` (not wired yet).

## bbrv3/
- `samsung-bbrv3-5.4-final.patch` — full BBRv3 5.10→5.4 port, 21 files,
  +3088/-16 (headers, sysctl/PLB, tcp_input, tcp_ipv4, cong, Kconfig,
  Makefile, uapi). `git apply --check` + `git diff --check` CLEAN.
- New files are INSIDE the final patch (`net/ipv4/tcp_bbr3.c`,
  `net/ipv4/tcp_plb.c`).
- `defconfig-bbrv3-fragment.txt` — `ADVANCED=y, BBR3=y, CUBIC=y, FQ=y`,
  default stays `cubic`.
- `config-proof.txt` — olddefconfig proof (all 5 symbols set, no drops).
- `build-log-tail.txt` — `tcp_bbr3.o` (585784 B) + `tcp_plb.o` (397312 B)
  compiled with `aarch64-linux-gnu-gcc`, `BUILD_EXIT=0`, zero errors.
- Planned inputs: `use_bbrv3` + `pin_bbrv3` (not wired yet).
