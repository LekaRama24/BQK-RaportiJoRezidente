"""
app.py — upload the raw survey export, get all report charts.

    python -m streamlit run app.py

Runs on your own computer: the files are processed in a temporary folder and deleted afterwards; nothing is sent
anywhere or kept. The data is cleaned on the way (same rules as the report workbook); only the charts come out.
"""
import os
import tempfile

import streamlit as st

import bqk
import figurat

TITLES = {f["file"]: f["title"] for f in figurat.FIGURAT}
SECTIONS = {"1": "1. Struktura e të anketuarve", "2": "2. Remitancat", "3": "3. Shpenzimet",
            "4": "4. Pranimet nga Kosova", "5": "5. Depozitat", "6": "6. Shpenzimi për person në ditë",
            "7": "7. Pikat kufitare", "A": "Aneks"}

st.set_page_config(page_title="Grafikët e raportit – Jo-rezidentët", layout="wide",
                   initial_sidebar_state="collapsed")

st.markdown("""
<style>
  #MainMenu, footer, header [data-testid="stToolbar"], [data-testid="stDecoration"],
  [data-testid="stStatusWidget"] {visibility: hidden; height: 0;}
  header {background: transparent;}
  .block-container {padding-top: 2rem; padding-bottom: 3rem; max-width: 1180px;}
  h1, h2, h3 {font-weight: 600; letter-spacing: -0.01em; color: #1F2328;}
  .topbar {border-bottom: 1px solid #D0D7DE; padding-bottom: 0.9rem; margin-bottom: 1.6rem;}
  .topbar .name {font-size: 1.55rem; font-weight: 600; color: #1F3864; margin-top: 0.15rem;}
  .topbar .desc {font-size: 0.92rem; color: #57606A; margin-top: 0.2rem;}
  .label {font-size: 0.78rem; letter-spacing: 0.06em; text-transform: uppercase; color: #57606A;
          margin: 0.2rem 0 0.4rem 0; font-weight: 600;}
  .stats {display: grid; grid-template-columns: repeat(5, 1fr); border: 1px solid #D0D7DE; margin: 0.4rem 0 1.2rem 0;}
  .stats > div {padding: 0.75rem 1rem; border-right: 1px solid #D0D7DE;}
  .stats > div:last-child {border-right: none;}
  .stats .k {font-size: 0.75rem; color: #57606A; text-transform: uppercase; letter-spacing: 0.05em;}
  .stats .v {font-size: 1.35rem; font-weight: 600; color: #1F2328; margin-top: 0.15rem;}
  .note {border-left: 3px solid #9A6700; background: #FFF8E5; padding: 0.7rem 1rem; font-size: 0.9rem;
         margin: 0.3rem 0 1rem 0; color: #1F2328;}
  .note.err {border-left-color: #CF222E; background: #FFEBE9;}
  .stButton button, .stDownloadButton button, .stFormSubmitButton button {border-radius: 3px; font-weight: 500;}
  [data-testid="stFileUploaderDropzone"] {border-radius: 3px; background: #F6F8FA;}
  /* main dataset: large drop area */
  .st-key-up_raw [data-testid="stFileUploaderDropzone"] {min-height: 190px; padding: 2rem 1.5rem;
      border: 1.5px dashed #8C959F; background: #F6F8FA; display: flex; align-items: center; justify-content: center;}
  .st-key-up_raw [data-testid="stFileUploaderDropzone"]:hover {border-color: #1F3864; background: #EEF2F7;}
  .st-key-up_raw [data-testid="stFileUploaderDropzone"]:not(:has([data-testid="stFileChip"])) {flex-direction: column; gap: 0.7rem;}
  .st-key-up_raw [data-testid="stFileUploaderDropzone"] > div {justify-content: center;}
  .st-key-up_raw [data-testid="stFileUploaderDropzone"] [data-testid="stBaseButton-secondary"] {font-size: 1rem; padding: 0.55rem 1.4rem;}
  .st-key-up_raw [data-testid="stFileUploaderDropzoneInstructions"] {font-size: 0.9rem; text-align: center;}
  .st-key-up_raw [data-testid="stFileChip"] {padding: 0.9rem 1.2rem; border: 1px solid #D0D7DE; background: #FFFFFF;}
  .st-key-up_raw [data-testid="stFileChip"] svg {width: 2rem; height: 2rem;}
  .st-key-up_raw [data-testid="stFileChipName"] {font-size: 1.15rem; font-weight: 600; max-width: 30rem;
      white-space: normal; overflow: visible; text-overflow: clip; word-break: break-all;}
  .st-key-up_raw [data-testid="stFileChip"] * {max-width: none;}
  .st-key-up_raw [data-testid="stFileChip"] div div:last-child {font-size: 0.9rem;}
  .st-key-up_raw label p {font-size: 1rem; font-weight: 600;}
  /* optional files: compact */
  .st-key-up_cb [data-testid="stFileUploaderDropzone"], .st-key-up_korr [data-testid="stFileUploaderDropzone"]
      {min-height: 0; padding: 0.25rem 0.5rem;}
  .st-key-up_cb [data-testid="stFileUploaderDropzoneInstructions"],
  .st-key-up_korr [data-testid="stFileUploaderDropzoneInstructions"] {display: none;}
  .st-key-up_cb button, .st-key-up_korr button {padding: 0.1rem 0.55rem; min-height: 0; font-size: 0.82rem;}
  .st-key-up_cb [data-testid="stFileChip"], .st-key-up_korr [data-testid="stFileChip"] {padding: 0.1rem 0.4rem;}
  .st-key-up_cb [data-testid="stFileChip"] svg, .st-key-up_korr [data-testid="stFileChip"] svg {width: 1rem; height: 1rem;}
  .st-key-up_cb [data-testid="stFileChipName"], .st-key-up_korr [data-testid="stFileChipName"] {font-size: 0.82rem;}
  .st-key-up_cb label p, .st-key-up_korr label p {font-size: 0.85rem; color: #57606A;}
  [data-testid="stImageCaption"] {font-size: 0.85rem; color: #1F2328; text-align: left;}
  .stTabs [data-baseweb="tab"] {font-size: 0.92rem;}
  table {font-size: 0.86rem;}
</style>
<div class="topbar">
  <div class="name">Shpenzimet e jo-rezidentëve në Kosovë</div>
  <div class="desc">Grafikët e raportit nga dataseti i anketës</div>
</div>
""", unsafe_allow_html=True)


def note(text, kind=""):
    st.markdown(f'<div class="note {kind}">{text}</div>', unsafe_allow_html=True)


def save(upload, folder):
    path = os.path.join(folder, upload.name)
    with open(path, "wb") as f:
        f.write(upload.getbuffer())
    return path


# ------------------------------------------------------------------------------------------------ input
with st.form("hyrja", border=False):
    left, right = st.columns([3, 2], gap="large")
    with left:
        st.markdown('<div class="label">Të dhënat</div>', unsafe_allow_html=True)
        raw = st.file_uploader("Dataseti (bruto ose i pastruar)", type=["xlsx", "xls", "csv"], key="up_raw")
        codebook = st.file_uploader("Codebook (opsional)", type=["xlsx"], key="up_cb",
                                    help="Rekomandohet për vitet e vjetra: kodet e shteteve dhe të pikave kufitare.")
    with right:
        st.markdown('<div class="label">Parametrat</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        viti = c1.number_input("Viti", min_value=0, max_value=2100, value=0, step=1,
                               help="0 = sipas datave të intervistave")
        periudha = c2.text_input("Periudha e anketës", "korrik–gusht")
        outliers = st.text_input("Outlier-at (referues)", "", placeholder="p.sh. 52, 144, 147")
        with st.expander("Opsione të tjera"):
            pragu = st.number_input("Pragu i shpenzimeve (€)", min_value=0, value=10000, step=500)
            pika = st.selectbox("Pika kufitare, nëse eksporti nuk e ka kolonën",
                                ["Eksporti e ka kolonën", "Aeroport", "Merdarë"])
            korr = st.file_uploader("Korrigjime manuale (CSV, opsional)", type=["csv"], key="up_korr")
    go = st.form_submit_button("Krijo grafikët", type="primary")

if go:
    if raw is None:
        note("Ngarkoni datasetin.", "err")
        st.stop()
    try:
        ol = [int(x) for x in outliers.replace(";", ",").replace(" ", ",").split(",") if x.strip()]
    except ValueError:
        note("Outlier-at duhet të jenë numra (referues), p.sh. 52, 144, 147.", "err")
        st.stop()
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp, st.spinner("Duke përpunuar të dhënat…"):
        try:
            r, out, made, skipped, zpath = bqk.run(
                save(raw, tmp), dalja=os.path.join(tmp, "grafiket"),
                codebook=save(codebook, tmp) if codebook else None,
                korrigjime=save(korr, tmp) if korr else None,
                viti=int(viti) or None, outliers=ol, pragu=float(pragu), periudha=periudha,
                pika={"Aeroport": "A", "Merdarë": "M"}.get(pika))
        except SystemExit as e:                     # e.g. the file is not a survey export
            note(str(e), "err")
            st.stop()
        except Exception as e:
            import traceback
            note(f"Grafikët nuk u krijuan: {type(e).__name__}: {e}", "err")
            with st.expander("Detajet teknike"):
                st.code(traceback.format_exc())
            st.stop()
        st.session_state["rez"] = {
            "r": r, "skipped": skipped, "file": raw.name,
            "zip": open(zpath, "rb").read(), "zipname": os.path.basename(zpath),
            "figs": [(f, open(os.path.join(out, f), "rb").read()) for f in made],
        }

# ------------------------------------------------------------------------------------------------ results
rez = st.session_state.get("rez")
if rez:
    r = rez["r"]
    st.divider()
    head, dl = st.columns([3, 1], vertical_alignment="bottom")
    head.markdown(f"### Rezultatet – {r['viti']}")
    head.caption(rez["file"])
    dl.download_button("Shkarko të gjithë grafikët (.zip)", rez["zip"], rez["zipname"], "application/zip",
                       type="primary", width="stretch")
    other = "".join(f", {v} {k}" for k, v in r["pikat_tjera"].items())
    st.markdown(f"""
    <div class="stats">
      <div><div class="k">Intervista</div><div class="v">{r['n_raw']:,}</div></div>
      <div><div class="k">Të vlefshme</div><div class="v">{r['n_db']:,}</div></div>
      <div><div class="k">Aeroport</div><div class="v">{r['n_A']:,}</div></div>
      <div><div class="k">Merdarë</div><div class="v">{r['n_M']:,}{other}</div></div>
      <div><div class="k">Grafikë</div><div class="v">{len(rez['figs'])} / {len(rez['figs']) + len(rez['skipped'])}</div></div>
    </div>""", unsafe_allow_html=True)

    if rez["skipped"] or r["paralajmerime"]:
        note(f"{len(rez['skipped'])} grafikë nuk u krijuan dhe {len(r['paralajmerime'])} çështje duhen kontrolluar. "
             "Shihni skedën <b>Kontrolli i të dhënave</b>." if rez["skipped"] else
             f"{len(r['paralajmerime'])} çështje duhen kontrolluar. Shihni skedën <b>Kontrolli i të dhënave</b>.")

    tab_g, tab_k = st.tabs(["Grafikët", "Kontrolli i të dhënave"])
    with tab_g:
        groups = {}
        for name, png in rez["figs"]:
            key = name.split("_")[1]
            groups.setdefault(SECTIONS.get(key, "Të tjera"), []).append((name, png))
        for section, figs in groups.items():
            st.markdown(f'<div class="label" style="margin-top:1.2rem">{section}</div>', unsafe_allow_html=True)
            cols = st.columns(2, gap="large")
            for i, (name, png) in enumerate(figs):
                with cols[i % 2]:
                    with st.container(border=True):
                        st.image(png, width="stretch")
                        st.download_button("Shkarko PNG", png, name, "image/png", key="dl_" + name,
                                           type="tertiary")
    with tab_k:
        if rez["skipped"]:
            st.markdown('<div class="label">Grafikë që nuk u krijuan</div>', unsafe_allow_html=True)
            st.table([{"Grafiku": TITLES.get(f, f), "Arsyeja": why} for f, why in rez["skipped"]])
        if r.get("te_pasigurta"):
            st.markdown('<div class="label">Kolona që nuk u përdorën</div>', unsafe_allow_html=True)
            st.table([{"Kolona": c, "Arsyeja": why} for c, why in r["te_pasigurta"].items()])
        if r["paralajmerime"]:
            st.markdown('<div class="label">Paralajmërime</div>', unsafe_allow_html=True)
            st.table([{"Kolona": w[1], "Përshkrimi": w[4].replace("KUJDES: ", "", 1)} for w in r["paralajmerime"]])
        if r["perjashtuar"]:
            st.markdown(f'<div class="label">Intervista të përjashtuara ({len(r["perjashtuar"])})</div>',
                        unsafe_allow_html=True)
            st.table([{"interview__key": k, "Arsyeja": a} for k, a in r["perjashtuar"]])
        if not (rez["skipped"] or r["paralajmerime"] or r["perjashtuar"]):
            st.write("Nuk ka çështje për kontroll.")
