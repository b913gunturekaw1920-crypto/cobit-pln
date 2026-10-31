"""Aplikasi web Streamlit: implementasi audit COBIT 5 untuk PT PLN (Persero).

Tugas 2 Audit Sistem Informasi.
Jalankan dengan:  streamlit run app.py
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------------
# DATA COBIT 5: 5 domain, 17 proses, 34 pertanyaan audit
# (sama dengan form audit pada Tugas 1: PLN, layanan pelanggan
#  dan tagihan digital)
# ---------------------------------------------------------------
DOMAINS = [
 {
  "code": "EDM",
  "name": "Evaluate, Direct and Monitor",
  "procs": [
   {
    "id": "EDM01",
    "name": "Ensure Governance Framework Setting and Maintenance",
    "q": [
     {
      "t": "Apakah terdapat kerangka tata kelola TI yang ditetapkan manajemen dan selaras dengan tujuan bisnis layanan pelanggan?",
      "e": "Dokumen kebijakan/kerangka tata kelola TI, SK pembentukan komite TI"
     },
     {
      "t": "Apakah peran dan tanggung jawab pengambilan keputusan terkait TI (termasuk aplikasi layanan pelanggan dan tagihan digital) telah ditetapkan secara jelas?",
      "e": "Struktur organisasi TI, matriks RACI, uraian jabatan"
     }
    ]
   },
   {
    "id": "EDM03",
    "name": "Ensure Risk Optimisation",
    "q": [
     {
      "t": "Apakah manajemen telah menetapkan batas toleransi risiko TI yang berkaitan dengan layanan pelanggan dan tagihan digital?",
      "e": "Dokumen risk appetite, kebijakan manajemen risiko"
     },
     {
      "t": "Apakah risiko TI dievaluasi secara berkala dan hasilnya dilaporkan kepada pimpinan?",
      "e": "Laporan profil risiko TI, notulen rapat manajemen risiko"
     }
    ]
   },
   {
    "id": "EDM05",
    "name": "Ensure Stakeholder Transparency",
    "q": [
     {
      "t": "Apakah terdapat mekanisme pelaporan kinerja layanan TI kepada pemangku kepentingan (pimpinan dan pelanggan)?",
      "e": "Laporan kinerja TI, dasbor layanan, laporan tahunan"
     },
     {
      "t": "Apakah kebutuhan dan umpan balik pemangku kepentingan terkait layanan digital diidentifikasi dan ditindaklanjuti?",
      "e": "Hasil survei kepuasan pelanggan, log tindak lanjut masukan"
     }
    ]
   }
  ]
 },
 {
  "code": "APO",
  "name": "Align, Plan and Organise",
  "procs": [
   {
    "id": "APO02",
    "name": "Manage Strategy",
    "q": [
     {
      "t": "Apakah terdapat rencana strategis TI yang selaras dengan strategi bisnis perusahaan?",
      "e": "Dokumen rencana strategis/roadmap TI, rencana jangka panjang perusahaan"
     },
     {
      "t": "Apakah rencana strategis TI ditinjau dan diperbarui secara berkala?",
      "e": "Riwayat revisi dokumen strategi, notulen reviu strategi"
     }
    ]
   },
   {
    "id": "APO07",
    "name": "Manage Human Resources",
    "q": [
     {
      "t": "Apakah kebutuhan kompetensi dan jumlah SDM TI dipetakan serta dipenuhi?",
      "e": "Analisis kebutuhan SDM, peta kompetensi, data kepegawaian TI"
     },
     {
      "t": "Apakah terdapat program pelatihan dan pengembangan kompetensi bagi personel TI?",
      "e": "Rencana dan realisasi pelatihan, sertifikat pelatihan"
     }
    ]
   },
   {
    "id": "APO12",
    "name": "Manage Risk",
    "q": [
     {
      "t": "Apakah risiko yang berkaitan dengan sistem layanan pelanggan dan tagihan digital diidentifikasi, dinilai, dan didokumentasikan?",
      "e": "Risk register, hasil penilaian risiko"
     },
     {
      "t": "Apakah terdapat rencana mitigasi risiko dengan penanggung jawab dan tenggat yang jelas?",
      "e": "Rencana tindak mitigasi, laporan pemantauan risiko"
     }
    ]
   },
   {
    "id": "APO13",
    "name": "Manage Security",
    "q": [
     {
      "t": "Apakah terdapat kebijakan keamanan informasi yang disahkan dan disosialisasikan kepada seluruh pegawai?",
      "e": "Kebijakan keamanan informasi, bukti sosialisasi"
     },
     {
      "t": "Apakah sistem manajemen keamanan informasi dijalankan dan dievaluasi secara berkala (misalnya mengacu pada ISO/IEC 27001)?",
      "e": "Dokumen SMKI, laporan audit keamanan internal, sertifikat jika ada"
     }
    ]
   }
  ]
 },
 {
  "code": "BAI",
  "name": "Build, Acquire and Implement",
  "procs": [
   {
    "id": "BAI03",
    "name": "Manage Solutions Identification and Build",
    "q": [
     {
      "t": "Apakah pengembangan atau pengadaan aplikasi mengikuti metodologi yang baku (analisis kebutuhan, desain, pengujian)?",
      "e": "Dokumen SDLC, spesifikasi kebutuhan, dokumen desain sistem"
     },
     {
      "t": "Apakah sistem diuji dan disetujui pengguna sebelum diluncurkan ke lingkungan produksi?",
      "e": "Skenario dan hasil uji (UAT), berita acara serah terima"
     }
    ]
   },
   {
    "id": "BAI06",
    "name": "Manage Changes",
    "q": [
     {
      "t": "Apakah setiap perubahan pada sistem atau infrastruktur diajukan, dinilai dampaknya, dan disetujui secara formal?",
      "e": "Formulir permintaan perubahan, catatan persetujuan change advisory board"
     },
     {
      "t": "Apakah terdapat prosedur perubahan darurat dan rencana pemulihan (rollback) jika perubahan gagal?",
      "e": "Prosedur perubahan darurat, rencana rollback, log perubahan"
     }
    ]
   },
   {
    "id": "BAI09",
    "name": "Manage Assets",
    "q": [
     {
      "t": "Apakah aset TI (perangkat keras, perangkat lunak, lisensi) tercatat lengkap dan diperbarui?",
      "e": "Inventaris aset TI, daftar lisensi"
     },
     {
      "t": "Apakah terdapat prosedur pemeliharaan dan penghapusan aset TI yang aman?",
      "e": "Jadwal pemeliharaan, berita acara penghapusan aset"
     }
    ]
   }
  ]
 },
 {
  "code": "DSS",
  "name": "Deliver, Service and Support",
  "procs": [
   {
    "id": "DSS01",
    "name": "Manage Operations",
    "q": [
     {
      "t": "Apakah prosedur operasional harian sistem (pemantauan, backup, penjadwalan) didokumentasikan dan dijalankan?",
      "e": "SOP operasional, jadwal dan log backup, log pemantauan sistem"
     },
     {
      "t": "Apakah kondisi infrastruktur (server, jaringan, pusat data) dipantau untuk mencegah gangguan?",
      "e": "Laporan pemantauan, bukti sistem monitoring"
     }
    ]
   },
   {
    "id": "DSS02",
    "name": "Manage Service Requests and Incidents",
    "q": [
     {
      "t": "Apakah terdapat kanal dan prosedur penanganan keluhan atau insiden layanan (misalnya kegagalan pembayaran atau gangguan aplikasi)?",
      "e": "SOP penanganan insiden, data tiket helpdesk/kontak layanan"
     },
     {
      "t": "Apakah waktu penyelesaian insiden diukur terhadap target tingkat layanan (SLA) dan dievaluasi?",
      "e": "Dokumen SLA, laporan insiden dan waktu penyelesaian"
     }
    ]
   },
   {
    "id": "DSS04",
    "name": "Manage Continuity",
    "q": [
     {
      "t": "Apakah terdapat rencana keberlangsungan layanan dan pemulihan bencana (BCP/DRP) untuk sistem kritis?",
      "e": "Dokumen BCP/DRP, analisis dampak bisnis"
     },
     {
      "t": "Apakah rencana pemulihan diuji secara berkala dan hasilnya didokumentasikan?",
      "e": "Laporan uji simulasi DRP, bukti perbaikan hasil uji"
     }
    ]
   },
   {
    "id": "DSS05",
    "name": "Manage Security Services",
    "q": [
     {
      "t": "Apakah akses pengguna ke sistem dan data pelanggan dikendalikan berdasarkan hak akses dan dikaji ulang secara berkala?",
      "e": "Matriks hak akses, log akses, hasil reviu hak akses"
     },
     {
      "t": "Apakah terdapat perlindungan terhadap ancaman keamanan dan perlindungan data pribadi pelanggan (misalnya enkripsi dan pemantauan keamanan)?",
      "e": "Konfigurasi keamanan, laporan uji penetrasi, kebijakan perlindungan data pribadi"
     }
    ]
   }
  ]
 },
 {
  "code": "MEA",
  "name": "Monitor, Evaluate and Assess",
  "procs": [
   {
    "id": "MEA01",
    "name": "Monitor, Evaluate and Assess Performance and Conformance",
    "q": [
     {
      "t": "Apakah indikator kinerja TI ditetapkan, diukur, dan dilaporkan secara berkala?",
      "e": "Daftar KPI TI, laporan pengukuran kinerja"
     },
     {
      "t": "Apakah hasil pengukuran kinerja digunakan sebagai dasar perbaikan layanan?",
      "e": "Notulen reviu kinerja, rencana tindak perbaikan"
     }
    ]
   },
   {
    "id": "MEA02",
    "name": "Monitor, Evaluate and Assess the System of Internal Control",
    "q": [
     {
      "t": "Apakah pengendalian internal TI dipantau dan dievaluasi, termasuk melalui audit internal?",
      "e": "Program dan laporan audit internal TI"
     },
     {
      "t": "Apakah temuan audit atau kelemahan pengendalian ditindaklanjuti sampai selesai?",
      "e": "Matriks tindak lanjut temuan audit, status penyelesaian"
     }
    ]
   },
   {
    "id": "MEA03",
    "name": "Monitor, Evaluate and Assess Compliance with External Requirements",
    "q": [
     {
      "t": "Apakah peraturan dan standar eksternal yang berlaku bagi TI perusahaan (termasuk UU Pelindungan Data Pribadi) diidentifikasi?",
      "e": "Daftar peraturan dan persyaratan kepatuhan"
     },
     {
      "t": "Apakah kepatuhan terhadap peraturan tersebut dinilai secara berkala dan hasilnya dilaporkan?",
      "e": "Laporan kepatuhan, hasil asesmen kepatuhan"
     }
    ]
   }
  ]
 }
]

SKALA = {
    0: "Incomplete Process",
    1: "Performed Process",
    2: "Managed Process",
    3: "Established Process",
    4: "Predictable Process",
    5: "Optimising Process",
}
JAWABAN = {"Ya": 1.0, "Sebagian": 0.5, "Tidak": 0.0}
TARGET_DEFAULT = 3

WARNA_STATUS = {
    "Tercapai": "#2e7d32",
    "Perlu perbaikan": "#ef8f00",
    "Prioritas perbaikan": "#c62828",
}


def semua_proses():
    """Daftar datar seluruh proses: (kode domain, proses)."""
    return [(d["code"], p) for d in DOMAINS for p in d["procs"]]


def status_gap(gap):
    """Kategori berdasarkan gap (target dikurangi level saat ini)."""
    if gap <= 0:
        return "Tercapai"
    if gap <= 1:
        return "Perlu perbaikan"
    return "Prioritas perbaikan"


def contoh_data():
    """Data CONTOH (simulasi) untuk mencoba program. Bukan hasil audit nyata."""
    level = {
        "EDM01": 2, "EDM03": 2, "EDM05": 3,
        "APO02": 3, "APO07": 2, "APO12": 2, "APO13": 3,
        "BAI03": 3, "BAI06": 2, "BAI09": 3,
        "DSS01": 3, "DSS02": 3, "DSS04": 2, "DSS05": 3,
        "MEA01": 2, "MEA02": 1, "MEA03": 3,
    }
    data = {}
    for _, p in semua_proses():
        lv = level[p["id"]]
        if lv >= 3:
            jawab = ["Ya", "Ya"]
        elif lv == 2:
            jawab = ["Ya", "Sebagian"]
        else:
            jawab = ["Sebagian", "Tidak"]
        data[p["id"]] = {"level": lv, "target": TARGET_DEFAULT, "jawaban": jawab}
    return data


def data_kosong(target=TARGET_DEFAULT):
    """Data awal: semua level 0 dan semua jawaban 'Tidak'."""
    return {
        p["id"]: {"level": 0, "target": target, "jawaban": ["Tidak"] * len(p["q"])}
        for _, p in semua_proses()
    }


def hitung_proses(data):
    """Hitung tabel detail per proses dari data input.

    data: {id_proses: {"level": 0-5, "target": 0-5, "jawaban": ["Ya"/"Sebagian"/"Tidak", ...]}}
    """
    baris = []
    for kode, p in semua_proses():
        if p["id"] not in data:
            raise ValueError(f"Data untuk proses {p['id']} belum diisi")
        isi = data[p["id"]]
        level, target = int(isi["level"]), int(isi["target"])
        if not (0 <= level <= 5 and 0 <= target <= 5):
            raise ValueError(f"Level/target {p['id']} harus 0 sampai 5")
        jawaban = isi["jawaban"]
        if len(jawaban) != len(p["q"]) or any(j not in JAWABAN for j in jawaban):
            raise ValueError(f"Jawaban {p['id']} tidak valid")
        kepatuhan = 100 * sum(JAWABAN[j] for j in jawaban) / len(jawaban)
        gap = target - level
        baris.append({
            "Domain": kode,
            "ID": p["id"],
            "Proses": p["name"],
            "Level": level,
            "Target": target,
            "Gap": gap,
            "Kepatuhan (%)": round(kepatuhan, 1),
            "Status": status_gap(gap),
        })
    return pd.DataFrame(baris)


def rekap_domain(detail):
    """Rekapitulasi per domain, ditambah baris rata-rata keseluruhan proses."""
    nama = {d["code"]: d["name"] for d in DOMAINS}
    baris = []
    for kode in [d["code"] for d in DOMAINS]:
        sub = detail[detail["Domain"] == kode]
        baris.append(_baris_rekap(kode, nama[kode], sub))
    baris.append(_baris_rekap("Rata-rata", "Seluruh proses", detail))
    return pd.DataFrame(baris)


def _baris_rekap(kode, nama, sub):
    level = sub["Level"].mean()
    target = sub["Target"].mean()
    gap = target - level
    return {
        "Domain": kode,
        "Nama Domain": nama,
        "Jumlah Proses": len(sub),
        "Rata-rata Level": round(level, 2),
        "Rata-rata Target": round(target, 2),
        "Gap": round(gap, 2),
        "Kepatuhan (%)": round(sub["Kepatuhan (%)"].mean(), 1),
        "Status": status_gap(gap),
    }


def grafik_radar(rekap):
    """Radar: level saat ini vs target untuk tiap domain."""
    d = rekap[rekap["Domain"] != "Rata-rata"]
    label = list(d["Domain"])
    sudut = np.linspace(0, 2 * np.pi, len(label), endpoint=False).tolist()
    sudut += sudut[:1]
    fig, ax = plt.subplots(figsize=(5.5, 5.5), subplot_kw={"polar": True})
    nilai = d["Rata-rata Level"].tolist() + d["Rata-rata Level"].tolist()[:1]
    target = d["Rata-rata Target"].tolist() + d["Rata-rata Target"].tolist()[:1]
    ax.plot(sudut, nilai, "-o", linewidth=2, color="#1f5fa8", label="Level saat ini")
    ax.fill(sudut, nilai, alpha=0.2, color="#1f5fa8")
    ax.plot(sudut, target, "--", linewidth=2, color="#c62828", label="Target")
    ax.set_xticks(sudut[:-1])
    ax.set_xticklabels(label, fontsize=11)
    ax.set_ylim(0, 5)
    ax.set_yticks(range(0, 6))
    ax.set_title("Level kapabilitas per domain COBIT 5", pad=18)
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))
    fig.tight_layout()
    return fig


def grafik_gap(detail):
    """Batang horizontal: gap tiap proses, diurutkan dari yang terbesar."""
    d = detail.sort_values(["Gap", "ID"], ascending=[True, False])
    fig, ax = plt.subplots(figsize=(7, 0.38 * len(d) + 1.4))
    warna = [WARNA_STATUS[s] for s in d["Status"]]
    ax.barh(d["ID"], d["Gap"], color=warna)
    for y, (g, lv) in enumerate(zip(d["Gap"], d["Level"])):
        ax.text(g + (0.05 if g >= 0 else -0.05), y, f"{g}  (level {lv})",
                va="center", ha="left" if g >= 0 else "right", fontsize=8)
    ax.axvline(0, color="#555", linewidth=0.8)
    ax.set_xlabel("Gap = target - level saat ini")
    ax.set_title("Gap kapabilitas per proses")
    ax.set_xlim(min(-1, d["Gap"].min() - 1), max(d["Gap"].max() + 1.5, 1.5))
    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in WARNA_STATUS.values()]
    ax.legend(handles, list(WARNA_STATUS), loc="lower right", fontsize=8)
    fig.tight_layout()
    return fig


def kesimpulan(detail, rekap):
    """Kesimpulan otomatis dalam bentuk daftar kalimat."""
    total = rekap[rekap["Domain"] == "Rata-rata"].iloc[0]
    domain = rekap[rekap["Domain"] != "Rata-rata"]
    terendah = domain.sort_values("Rata-rata Level").iloc[0]
    tertinggi = domain.sort_values("Rata-rata Level").iloc[-1]
    prioritas = detail[detail["Status"] == "Prioritas perbaikan"].sort_values("Gap", ascending=False)
    tercapai = detail[detail["Status"] == "Tercapai"]
    baris = [
        f"Rata-rata level kapabilitas seluruh proses adalah {total['Rata-rata Level']:.2f} "
        f"dari target {total['Rata-rata Target']:.2f} (gap {total['Gap']:.2f}), "
        f"atau setara '{SKALA[int(round(total['Rata-rata Level']))]}'.",
        f"Domain dengan level tertinggi adalah {tertinggi['Domain']} ({tertinggi['Rata-rata Level']:.2f}); "
        f"yang terendah adalah {terendah['Domain']} ({terendah['Rata-rata Level']:.2f}).",
        f"{len(tercapai)} dari {len(detail)} proses sudah mencapai target.",
    ]
    if len(prioritas):
        daftar = ", ".join(f"{r.ID} (gap {r.Gap})" for r in prioritas.itertuples())
        baris.append(f"Proses yang menjadi prioritas perbaikan (gap lebih dari 1): {daftar}.")
    else:
        baris.append("Tidak ada proses dengan gap lebih dari 1.")
    return baris

# ---------------------------------------------------------------
# ANTARMUKA STREAMLIT
# ---------------------------------------------------------------
import io

import streamlit as st

st.set_page_config(page_title="Audit COBIT 5 - PLN", layout="wide")


def kunci(jenis, id_proses, i=None):
    return f"{jenis}_{id_proses}" if i is None else f"{jenis}_{id_proses}_{i}"


def isi_state(data):
    """Tulis data penilaian ke session_state (dipakai tombol contoh/reset)."""
    for _, p in semua_proses():
        isi = data[p["id"]]
        st.session_state[kunci("lvl", p["id"])] = isi["level"]
        st.session_state[kunci("tgt", p["id"])] = isi["target"]
        for i, j in enumerate(isi["jawaban"]):
            st.session_state[kunci("ans", p["id"], i)] = j


def muat_contoh():
    isi_state(contoh_data())
    st.session_state["mode_contoh"] = True


def reset_semua():
    isi_state(data_kosong())
    st.session_state["mode_contoh"] = False


def ambil_data():
    data = {}
    for _, p in semua_proses():
        data[p["id"]] = {
            "level": st.session_state[kunci("lvl", p["id"])],
            "target": st.session_state[kunci("tgt", p["id"])],
            "jawaban": [st.session_state[kunci("ans", p["id"], i)] for i in range(len(p["q"]))],
        }
    return data


if "siap" not in st.session_state:
    isi_state(data_kosong())
    st.session_state["mode_contoh"] = False
    st.session_state["siap"] = True

# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("Identitas")
    nama = st.text_input("Nama", placeholder="[Nama Lengkap]")
    nim = st.text_input("NIM", placeholder="[NIM]")
    kelas = st.text_input("Kelas", placeholder="[Kelas]")
    st.divider()
    st.header("Data")
    st.button("Muat data contoh", on_click=muat_contoh, width="stretch")
    st.button("Reset semua isian", on_click=reset_semua, width="stretch")
    st.caption("Data contoh hanya simulasi untuk mencoba aplikasi, bukan hasil audit nyata PLN.")
    st.divider()
    st.header("Skala kapabilitas")
    for k, v in SKALA.items():
        st.caption(f"**{k}** - {v}")

st.title("Audit Sistem Informasi dengan COBIT 5")
st.markdown("**Objek:** PT PLN (Persero) - sistem layanan pelanggan dan tagihan digital")

if st.session_state.get("mode_contoh"):
    st.warning(
        "Isian awal berasal dari data contoh (simulasi). Ubah nilai sesuai hasil audit "
        "sebenarnya atau tekan Reset sebelum dipakai sebagai laporan."
    )

tab_input, tab_hasil, tab_info = st.tabs(["Input penilaian", "Hasil dan rekap", "Tentang aplikasi"])

# ---------------- Tab input ----------------
with tab_input:
    st.write(
        "Jawab setiap pertanyaan audit (Ya, Sebagian, atau Tidak), lalu tentukan "
        "level kapabilitas dan target level untuk setiap proses."
    )
    tab_domain = st.tabs([f"{d['code']}" for d in DOMAINS])
    for tab, d in zip(tab_domain, DOMAINS):
        with tab:
            st.subheader(f"{d['code']} - {d['name']}")
            for p in d["procs"]:
                with st.container(border=True):
                    st.markdown(f"**{p['id']}** - {p['name']}")
                    kiri, kanan = st.columns([3, 1])
                    with kiri:
                        for i, q in enumerate(p["q"]):
                            st.radio(
                                q["t"], list(JAWABAN), key=kunci("ans", p["id"], i),
                                horizontal=True, help=f"Bukti yang diperiksa: {q['e']}",
                            )
                    with kanan:
                        st.slider("Level saat ini (0-5)", 0, 5, key=kunci("lvl", p["id"]))
                        st.slider("Target level (0-5)", 0, 5, key=kunci("tgt", p["id"]))

# ---------------- Tab hasil ----------------
with tab_hasil:
    detail = hitung_proses(ambil_data())
    rekap = rekap_domain(detail)
    total = rekap[rekap["Domain"] == "Rata-rata"].iloc[0]

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Rata-rata level", f"{total['Rata-rata Level']:.2f}")
    m2.metric("Rata-rata target", f"{total['Rata-rata Target']:.2f}")
    m3.metric("Gap", f"{total['Gap']:.2f}")
    m4.metric("Kepatuhan", f"{total['Kepatuhan (%)']:.1f}%")

    st.subheader("Rekapitulasi per domain")
    st.dataframe(rekap, hide_index=True, width="stretch")

    g1, g2 = st.columns(2)
    with g1:
        st.pyplot(grafik_radar(rekap))
    with g2:
        st.pyplot(grafik_gap(detail))

    st.subheader("Detail per proses")
    st.dataframe(detail, hide_index=True, width="stretch")

    st.subheader("Kesimpulan otomatis")
    for kalimat in kesimpulan(detail, rekap):
        st.markdown(f"- {kalimat}")

    st.subheader("Unduh hasil")
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as xl:
        pd.DataFrame({
            "Keterangan": ["Nama", "NIM", "Kelas", "Objek audit"],
            "Isi": [nama or "[Nama]", nim or "[NIM]", kelas or "[Kelas]",
                    "PT PLN (Persero) - layanan pelanggan dan tagihan digital"],
        }).to_excel(xl, sheet_name="Identitas", index=False)
        rekap.to_excel(xl, sheet_name="Rekap Domain", index=False)
        detail.to_excel(xl, sheet_name="Detail Proses", index=False)
    d1, d2 = st.columns(2)
    d1.download_button(
        "Unduh Excel (.xlsx)", buf.getvalue(), "hasil_audit_cobit_pln.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        width="stretch",
    )
    d2.download_button(
        "Unduh detail (.csv)", detail.to_csv(index=False).encode("utf-8"),
        "detail_audit_cobit_pln.csv", "text/csv", width="stretch",
    )

# ---------------- Tab info ----------------
with tab_info:
    st.markdown(
        """
**Cara kerja**
1. Setiap proses COBIT memiliki dua pertanyaan audit. Jawaban Ya bernilai 1, Sebagian 0,5, dan Tidak 0, lalu dirata-ratakan menjadi persentase kepatuhan.
2. Auditor menentukan level kapabilitas (0-5) dan target level tiap proses. Gap = target dikurangi level saat ini.
3. Status: **Tercapai** (gap 0 atau kurang), **Perlu perbaikan** (gap 1), **Prioritas perbaikan** (gap lebih dari 1).
4. Rekap domain dihitung dari rata-rata proses di dalam domain. Baris rata-rata keseluruhan dihitung dari seluruh proses.

**Domain COBIT 5 yang dinilai:** EDM, APO, BAI, DSS, dan MEA (17 proses, 34 pertanyaan), sama dengan form audit pada Tugas 1.
"""
    )
