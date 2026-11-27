# bqkcharts

**Shqip** · [English](#english)

## Grafikët e raportit mbi shpenzimet e jo-rezidentëve

Ngarkoni datasetin e anketës mbi shpenzimet e jo-rezidentëve në Kosovë (Aeroport / Merdarë), qoftë eksporti bruto
ose një workbook i pastruar, dhe merrni të gjithë grafikët e raportit si skedarë PNG. Të dhënat pastrohen gjatë
procesit me të njëjtat rregulla si workbook-u i raportit, por del vetëm grafikët.

Mjeti punon për çdo vit të anketës. Çdo gjë që ndryshon nga viti në vit (emrat e kolonave, kodet, etiketat) gjendet
te `pastrimi/skema.json` dhe te codebook-u i vitit, jo në kod. Kolonat njihen edhe sipas përmbajtjes, jo vetëm sipas
titullit, prandaj një titull i zhvendosur, bosh, i shkruar gabim ose i lëvizur nuk e ndal procesin. Çdo rregullim
shënohet te paralajmërimet.

**Rregulli: asnjë grafik nuk krijohet nga një kolonë për të cilën mjeti nuk është i sigurt.** Çdo kolonë kontrollohet
sipas përmbajtjes (datat duhet të jenë data, kodet duhet të jenë kode të vlefshme…) dhe sipas rregullave të pyetësorit:
vendet e vizituara vetëm për ata që kanë udhëtuar jashtë, kanalet e remitancave vetëm për ata që dërgojnë para, forma e
depozitës vetëm për ata që kanë depozitë, pasaportat e përziera vetëm për grupet e përziera. Kontrollohen edhe kodet e
pikës kufitare: nëse udhëtarët e Aeroportit dalin të shpenzojnë më pak para mbërritjes se ata që vijnë me rrugë, kodet
trajtohen si të këmbyera. Një kolonë që nuk e kalon kontrollin nuk përdoret, dhe çdo grafik që varet prej saj
anashkalohet me arsyen përkatëse. Skeda **Kontrolli i të dhënave** në aplikacion tregon cilat kolona nuk u përdorën
dhe pse.

> **Këtu nuk ruhen të dhëna të anketës.** Eksportet, codebook-ët dhe grafikët përjashtohen nga `.gitignore`.

### Windows: klikim i dyfishtë

Instaloni Python një herë nga python.org (gjatë instalimit zgjidhni **"Add python.exe to PATH"**). Pastaj klikoni dy
herë `start_app.bat`: herën e parë përgatit gjithçka vetë (1–3 minuta), ndërsa herëve të tjera e hap aplikacionin
menjëherë në shfletues. Mbajeni dritaren e zezë të hapur gjatë përdorimit; mbylleni për ta ndalur.

### Përgatitja me dorë (Mac / Linux, ose Windows pa .bat)

```bash
cd bqkcharts
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
```

### Përdorimi: aplikacioni

```bash
source .venv/bin/activate
python -m streamlit run app.py
```

Hapet një faqe në shfletues:

1. ngarkoni datasetin (dhe codebook-un, i rekomanduar për vitet e vjetra);
2. sipas nevojës plotësoni outlier-at, pragun dhe periudhën e anketës;
3. klikoni **Krijo grafikët**.

Të gjithë grafikët shfaqen në ekran, secili me butonin e vet për shkarkim, dhe ka një buton për t'i shkarkuar të gjithë
si .zip. Gjithçka punon në kompjuterin tuaj: skedarët e ngarkuar përpunohen në një dosje të përkohshme dhe fshihen.

### Përdorimi: një komandë

```bash
python bqk.py data/Dataset_Total_Final.xlsx --codebook data/Codebook.xlsx --outliers 52 144 147 46 41
```

→ dosja `grafiket_<viti>/` me të gjithë grafikët dhe `grafiket_<viti>.zip`.

| Opsioni | Kuptimi |
|---|---|
| `--codebook SKEDARI` | codebook-u; fleta e vitit të anketës (ose e fundit para tij) jep kodet |
| `--viti 2027` | viti i anketës (parazgjedhje: nga datat e intervistave) |
| `--dalja DOSJA` | dosja e rezultateve |
| `--outliers 52 144 …` | numrat `referues` që shënohen si outlier |
| `--pragu 10000` | pragu për "shpenzime ≤ 10,000 €" |
| `--korrigjime SKEDARI` | korrigjime manuale (shih `pastrimi/korrigjime_shembull.csv`) |
| `--periudha "korrik–gusht"` | periudha e anketës që shkruhet te burimi i grafikut |
| `--pika A` / `--pika M` | vetëm nëse eksporti nuk ka kolonën e pikës kufitare (skedar vetëm për një pikë) |
| `--fleta EMRI` | fleta e eksportit (parazgjedhje: ajo që i ngjan më shumë anketës) |

### Kur eksporti i një viti të ri është ndryshe

Ndryshoni `pastrimi/skema.json`, jo kodin:

* **një kolonë ka emër të ri:** shtojeni te lista e saj nën `"kolonat"` (shkronjat e mëdha, theksat dhe hapësirat nuk
  kanë rëndësi);
* **kodet e pikës kufitare kanë kuptim tjetër:** shtoni vitin nën `"pika_kufitare"`, p.sh. `"2018": {"1": "A", "2": "M"}`
  (lexohet automatikisht nëse codebook-u ka `1A` / `2M`);
* **një pyetje e re Po/Jo:** shtojeni te `"po_jo"`;
* **një shtet i ri:** jepni codebook-un, ose shtoni kodin nën `"kodet_e_shteteve_parazgjedhje"`.

### Struktura

```
app.py                    aplikacioni (Streamlit)
bqk.py                    një komandë: dataseti → grafikët
start_app.bat             hap aplikacionin në Windows
.streamlit/config.toml    ngjyrat dhe pamja e aplikacionit
pastrimi/
  pastro_dataset.py       pastrimi i të dhënave (hap i ndërmjetëm)
  skema.json              rregullat e viteve (emrat e kolonave, kodet, etiketat)
  korrigjime_shembull.csv formati i skedarit të korrigjimeve manuale
grafiket/
  bqk_grafiket.py         paleta, llojet e grafikëve, faqosja
  figurat.py              grafikët e raportit
data/                     skedarët tuaj (nuk ngarkohen në GitHub)
```

---

<a id="english"></a>

**English** · [Shqip](#bqkcharts)

## Charts for the report on non-resident spending

Upload the dataset of the survey of non-resident spending in Kosovo (Airport / Merdarë), either the raw export or a
cleaned workbook, and get all the report charts back as PNG files. The data is cleaned along the way with the same
rules as the report workbook, but only the charts come out.

It works for any survey year. Everything that changes between years (column names, codes, labels) is in
`pastrimi/skema.json` and the year's codebook, not in the code. Columns are recognised by their contents as well as
their headers, so a shifted, blank, misspelled or moved header does not stop the run. Every fix is listed in the
warnings.

**Rule: no chart is ever drawn from a column the tool is not sure about.** Every column is checked by its contents
(dates must be dates, codes must be valid codes…) and against the questionnaire's skip patterns: countries visited
only for those who went abroad, remittance channels only for those who send money, deposit form only for those with a
deposit, mixed passports only for mixed groups. Border-point codes are checked too: if Airport travellers seem to spend
less before arriving than road travellers, the codes are treated as reversed. A column that fails is not used, and
every chart that needs it is skipped with the reason. The **Kontrolli i të dhënave** tab in the app lists which columns
were not used and why.

> **No survey data is stored here.** Exports, codebooks and charts are excluded by `.gitignore`.

### Windows: double-click

Install Python from python.org once (tick **"Add python.exe to PATH"** in the installer). Then double-click
`start_app.bat`: the first time it sets everything up by itself (1–3 minutes); every time after, it opens the app in
the browser straight away. Keep the black window open while you use the app; close it to stop.

### Setup by hand (Mac / Linux, or Windows without the .bat)

```bash
cd bqkcharts
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
```

### Use: the app

```bash
source .venv/bin/activate
python -m streamlit run app.py
```

A page opens in the browser:

1. upload the dataset (and the codebook, recommended for older years);
2. optionally fill in the outliers, threshold and survey period;
3. click **Krijo grafikët**.

All charts appear on screen, each with its own download button, and there is a button to download them all as a
.zip. Everything runs on your own computer: uploaded files are processed in a temporary folder and deleted.

### Use: one command

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
| `--pragu 10000` | threshold for "spending ≤ 10,000 €" |
| `--korrigjime FILE` | manual corrections (see `pastrimi/korrigjime_shembull.csv`) |
| `--periudha "korrik–gusht"` | survey period printed in the chart source line |
| `--pika A` / `--pika M` | only if the export has no border-point column (a file for one point only) |
| `--fleta NAME` | sheet of the export (default: the one that looks most like the survey) |

### When a new year's export is different

Edit `pastrimi/skema.json`, not the code:

* **a column has a new name:** add it to its list under `"kolonat"` (case, accents and spaces don't matter);
* **border-point codes mean something else:** add the year under `"pika_kufitare"`, e.g. `"2018": {"1": "A", "2": "M"}`
  (read automatically if the codebook shows `1A` / `2M`);
* **a new Yes/No question:** add it to `"po_jo"`;
* **a new country:** pass the codebook, or add the code under `"kodet_e_shteteve_parazgjedhje"`.

### Structure

```
app.py                    the app (Streamlit)
bqk.py                    one command: dataset → charts
start_app.bat             starts the app on Windows
.streamlit/config.toml    colours and look of the app
pastrimi/
  pastro_dataset.py       data cleaning (intermediate step)
  skema.json              year rules (column names, codes, labels)
  korrigjime_shembull.csv format of the manual corrections file
grafiket/
  bqk_grafiket.py         palette, chart types, layout
  figurat.py              the report figures
data/                     your files (not uploaded to GitHub)
```


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
