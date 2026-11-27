# bqkcharts: grafikët e raportit të jo-rezidentëve

Upload the raw export of the BQK survey of non-resident spending in Kosovo (Aeroport / Merdarë) and get all the report
charts back as PNG files. The data is cleaned along the way with the same rules as the report workbook, but only the
charts come out.

It works for any survey year. Everything that changes between years (column names, codes, labels) is in
`pastrimi/skema.json` and the year's codebook, not in the code. Columns are recognised by their contents as well as
their headers, so a shifted, blank, misspelled or moved header does not stop the run. Every fix is listed in the
warnings.

**Rule: no chart is ever drawn from a column the code is not sure about.** Every column is checked by its contents
(dates must be dates, codes must be valid codes…) and against the questionnaire's skip patterns (countries visited
only for those who went abroad, remittance channels only for those who send money, deposit form only for those with a
deposit, mixed passports only for mixed groups). Border-point codes are checked too: if Airport travellers seem to spend
less before arriving than road travellers, the codes are treated as reversed. A column that fails is not used, and
every chart that needs it is skipped with the reason. The sheet `Cilesia` of the intermediate workbook (and the app)
lists, for each question, which export column was used, how it was found, and whether it was trusted.

> **No survey data is stored here.** Exports, codebooks and charts are excluded by `.gitignore`.

## Windows: double-click

Install Python from python.org once (tick **"Add python.exe to PATH"** in the installer). Then double-click
`start_app.bat`: the first time it sets everything up by itself (1–3 minutes), every time after it opens the app in
the browser straight away. Keep the black window open while you use the app; close it to stop.

## Setup by hand (Mac / Linux, or Windows without the .bat)

```bash
cd bqkcharts
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Use: upload page

```bash
source .venv/bin/activate
python -m streamlit run app.py
```

A page opens in the browser:

1. upload the raw export (and the codebook, recommended for older years);
2. optionally fill in the outliers, threshold and survey period;
3. click **Krijo grafikët**.

All charts appear on screen, each with its own download button, and there is a button to download them all as a
.zip. Everything runs on your own computer: uploaded files are processed in a temporary folder and deleted.

## Use: one command

```bash
python bqk.py data/Dataset_Total_Final.xlsx --codebook data/Codebook.xlsx --outliers 52 144 147 46 41
```

→ folder `grafiket_<year>/` with every chart and `grafiket_<year>.zip`.

| Option | Meaning |
|---|---|
| `--codebook FILE` | codebook workbook; the sheet of the survey year (or the latest earlier one) gives the codes |
| `--viti 2027` | survey year (default: from the interview dates) |
| `--dalja FOLDER` | output folder |
| `--outliers 52 144 …` | `referues` numbers marked as outliers |
| `--pragu 10000` | threshold for "shpenzime ≤ 10,000 €" |
| `--korrigjime FILE` | manual corrections (see `pastrimi/korrigjime_shembull.csv`) |
| `--periudha "korrik–gusht"` | survey period printed in the chart source line |
| `--pika A` / `--pika M` | only if the export has no border-point column (a file for one point only) |
| `--fleta NAME` | sheet of the export (default: the first) |

## When a new year's export is different

Edit `pastrimi/skema.json`, not the code:

* **a column has a new name:** add it to its list under `"kolonat"` (case, accents and spaces don't matter);
* **border-point numbers mean something else:** add the year under `"pika_kufitare"`, e.g. `"2018": {"1": "A", "2": "M"}`
  (read automatically if the codebook shows `1A` / `2M`);
* **a new Po/Jo question:** add it to `"po_jo"`;
* **a new country:** pass the codebook, or add the code under `"kodet_e_shteteve_parazgjedhje"`.

## Structure

```
app.py                    upload page (Streamlit)
bqk.py                    one command: raw export → charts
start_app.bat             starts the upload page on Windows
pastrimi/
  pastro_dataset.py       cleaning (intermediate step)
  skema.json              year rules (column names, codes, labels)
  korrigjime_shembull.csv format of the manual corrections file
grafiket/
  bqk_grafiket.py         palette, chart types, layout
  figurat.py              the report figures
data/                     your files (not committed)
```
