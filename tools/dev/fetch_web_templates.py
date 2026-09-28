#!/usr/bin/env python3
"""
Lädt NUR die Web-Export-Templates (≈ 20 MB) aus dem 1,3-GB-Template-Archiv von Godot,
per HTTP-Range-Anfragen auf das ZIP-Inhaltsverzeichnis. Nur Standardbibliothek.

Aufruf: python3 tools/dev/fetch_web_templates.py 4.7.2 [ziel_ordner] [--desktop]
  --desktop: zusätzlich Linux- und Windows-Release-Vorlagen (P09-T09, je ~80 MB)
Ziel-Standard (Linux): ~/.local/share/godot/export_templates/<version>.stable/
"""
import os
import struct
import sys
import urllib.request
import zlib

WANT = ("version.txt", "web_nothreads_release.zip", "web_nothreads_debug.zip")
DESKTOP = ("linux_release.x86_64", "windows_release_x86_64.exe")


def main() -> int:
    global WANT
    if "--desktop" in sys.argv:
        sys.argv.remove("--desktop")
        WANT = WANT + DESKTOP
    ver = sys.argv[1] if len(sys.argv) > 1 else "4.7.2"
    dst = sys.argv[2] if len(sys.argv) > 2 else os.path.expanduser(
        f"~/.local/share/godot/export_templates/{ver}.stable")
    url = (f"https://github.com/godotengine/godot/releases/download/{ver}-stable/"
           f"Godot_v{ver}-stable_export_templates.tpz")

    def rng(a: int, b: int) -> bytes:
        req = urllib.request.Request(url, headers={"Range": f"bytes={a}-{b}"})
        return urllib.request.urlopen(req).read()

    size = int(urllib.request.urlopen(urllib.request.Request(url, method="HEAD")).headers["Content-Length"])
    tail = rng(size - 70000, size - 1)
    i = tail.rfind(b"PK\x05\x06")
    cd_size, cd_off = struct.unpack("<II", tail[i + 12:i + 20])
    j = tail.rfind(b"PK\x06\x06")
    if cd_off == 0xFFFFFFFF and j >= 0:
        cd_size, cd_off = struct.unpack("<QQ", tail[j + 40:j + 56])
    cd = rng(cd_off, cd_off + cd_size - 1)
    os.makedirs(dst, exist_ok=True)
    p, got = 0, 0
    while p < len(cd) and cd[p:p + 4] == b"PK\x01\x02":
        meth, = struct.unpack("<H", cd[p + 10:p + 12])
        csz, usz = struct.unpack("<II", cd[p + 20:p + 28])
        nl, el, cl = struct.unpack("<HHH", cd[p + 28:p + 34])
        off, = struct.unpack("<I", cd[p + 42:p + 46])
        name = cd[p + 46:p + 46 + nl].decode()
        extra = cd[p + 46 + nl:p + 46 + nl + el]
        q = 0
        while q < len(extra):
            hid, hl = struct.unpack("<HH", extra[q:q + 4])
            d, k = extra[q + 4:q + 4 + hl], 0
            if hid == 1:
                if usz == 0xFFFFFFFF:
                    usz, = struct.unpack("<Q", d[k:k + 8]); k += 8
                if csz == 0xFFFFFFFF:
                    csz, = struct.unpack("<Q", d[k:k + 8]); k += 8
                if off == 0xFFFFFFFF:
                    off, = struct.unpack("<Q", d[k:k + 8]); k += 8
            q += 4 + hl
        if os.path.basename(name) in WANT:
            lh = rng(off, off + 29)
            lnl, lel = struct.unpack("<HH", lh[26:30])
            data = rng(off + 30 + lnl + lel, off + 30 + lnl + lel + csz - 1)
            out = zlib.decompress(data, -15) if meth == 8 else data
            with open(os.path.join(dst, os.path.basename(name)), "wb") as f:
                f.write(out)
            print(f"  ✔ {os.path.basename(name)} ({len(out) // 1024} KB)")
            got += 1
        p += 46 + nl + el + cl
    print(f"Web-Templates → {dst}")
    return 0 if got == len(WANT) else 1


if __name__ == "__main__":
    sys.exit(main())
