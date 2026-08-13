from pathlib import Path

p = Path("build_kernel_zip.sh")
s = p.read_text()

# build section
s = s.replace(
    '    CC="${CLANG_DIR}/bin/clang" \\\n',
    '    CC="${CLANG_DIR}/bin/clang" \\\n'
)

# remove duplicate/old cross compile leftovers
s = s.replace(
    '    CROSS_COMPILE=aarch64-linux-gnu- \\\n',
    '    CROSS_COMPILE="${TOOLCHAIN_DIR}/gcc/linux-x86/aarch64/aarch64-linux-android-4.9/bin/aarch64-linux-android-" \\\n'
)

# modules_install section exact fix
s = s.replace(
    '    CROSS_COMPILE=aarch64-linux-gnu- \\\n    STRIP="${CLANG_DIR}/bin/llvm-strip" \\\n',
    '    CROSS_COMPILE="${TOOLCHAIN_DIR}/gcc/linux-x86/aarch64/aarch64-linux-android-4.9/bin/aarch64-linux-android-" \\\n    STRIP="${CLANG_DIR}/bin/llvm-strip" \\\n'
)

p.write_text(s)

print("done")
