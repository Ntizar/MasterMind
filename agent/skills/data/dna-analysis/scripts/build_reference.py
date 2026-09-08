#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convierte el panel GrafAnc (AncSnpPopAFs.txt.gz) a un binario compacto para la web.
Cada SNP: chr(u8) pos37(u32) rs(u32) ref(u8) alt(u8) afs[26](u16). AFs cuantificadas a uint16
(clamp [1,65534] para evitar log(0)=-Inf -> NaN). Resultado gzip.
Cabecera: magic(6) 'DNAANC' + version(u8) + n_snps(u32 LE) = 11 bytes; registros desde el byte 11.
Registro = 1+4+4+1+1+52 = 63 bytes.
"""
import gzip, struct, os

SRC = r"C:\Users\d_ant\dna_work\grafanc\AncSnpPopAFs.txt.gz"
OUT = r"C:\Users\d_ant\Projects\dna-analyzer\data\panel.bin.gz"
BASE = {'A':0,'C':1,'G':2,'T':3}

buf = bytearray()
buf += b'DNAANC'
buf += struct.pack('<B', 1)          # version
buf += struct.pack('<I', 0)          # placeholder n_snps
rows = 0
with gzip.open(SRC,'rt',encoding='utf-8') as f:
    f.readline()  # header
    for line in f:
        if not line.strip(): continue
        p = line.rstrip('\n').split('\t')
        if len(p) < 32: continue
        chr_s = p[0]; pos = int(p[1]); rs = int(p[3])
        ref = BASE.get(p[4],0); alt = BASE.get(p[5],0)
        afs = [max(1,min(65534,int(round(float(p[6+i])*65535)))) for i in range(26)]
        buf += struct.pack('<B', int(chr_s) if chr_s.isdigit() else 0)
        buf += struct.pack('<I', pos)
        buf += struct.pack('<I', rs)
        buf += struct.pack('<BB', ref, alt)
        buf += struct.pack('<'+'H'*26, *afs)
        rows += 1

buf[7:11] = struct.pack('<I', rows)
with gzip.open(OUT,'wb',compresslevel=9) as g:
    g.write(buf)
print(f"SNPs={rows} binario={len(buf)/1e6:.1f}MB gzip={os.path.getsize(OUT)/1e6:.1f}MB -> {OUT}")
