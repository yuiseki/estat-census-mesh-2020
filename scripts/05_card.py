#!/usr/bin/env python3
"""Write data/README.md (the Hub card), data/LICENSE and data/provenance.yaml.

Counts come from the manifest of the newest run under data/raw/ and from data/parquet/.

    uv run python scripts/05_card.py
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
CC = "https://creativecommons.org/licenses/by/4.0/legalcode.ja"
TERMS = "https://www.e-stat.go.jp/terms-of-use"
GIS_TERMS = "https://www.e-stat.go.jp/gis-terms"
PAGE = "https://www.e-stat.go.jp/gis/statmap-search?page=1&type=1&toukeiCode=00200521&toukeiYear=2020&aggregateUnit=S&serveyId=S002005112020&statsId=T001100"


def facts() -> dict:
    d = sorted((DATA / "raw").glob("*/MANIFEST.json"))[-1].parent
    m = json.loads((d / "MANIFEST.json").read_text())
    cols = json.loads((DATA / "parquet" / "columns.json").read_text())
    files = m["files"]
    return {
        "run": d.name,
        "files": len(files),
        "bytes": sum(v["bytes"] for v in files.values()),
        "rows": sum(v["rows"] for v in files.values()),
        "updated": sorted({v["listed_updated"] for v in files.values()}),
        "fetched": min(v["fetched_at"] for v in files.values())[:10],
        "cols": cols,
    }


def card(f: dict) -> str:
    tables = "\n".join(
        f"| `{k}` | {v['datum']} | {v['name']} | {len(v['columns'])} | {v['rows']:,} |"
        for k, v in f["cols"].items()
    )
    return f"""---
license: cc-by-4.0
license_name: cc-by-4.0
license_link: {CC}
language:
- ja
tags:
- census
- japan
- grid-square
- mesh
- population
- e-stat
pretty_name: 2020 Japan census, 1 km grid-square statistics
---

# estat-census-mesh-2020

The 2020 census (令和2年国勢調査) of Japan, tabulated by 3rd-order grid square (the 1 km
mesh, 基準地域メッシュ), as published by the Statistics Bureau of Japan through e-Stat's
statistical GIS. {len(f["cols"])} tables x 47 prefectures = {f["files"]} files, {f["rows"]:,}
rows, fetched on {f["fetched"]} (the source lists them as updated {", ".join(f["updated"])}).

Source: 政府統計の総合窓口 (e-Stat) 地図で見る統計 (統計GIS), <{PAGE}>.

Credit (出典): 政府統計の総合窓口(e-Stat) (https://www.e-stat.go.jp/), 「令和2年国勢調査」
(総務省統計局). The Parquet files are converted from the source files (encoding, one table per
file); credit them as 「令和2年国勢調査」(総務省統計局) を加工して作成.

## Two geodetic datums, two sets of tables

The source publishes every table twice: on JGD2000 and on JGD2011. The two are not the same
data. For prefectures 02 to 21 (Aomori to Gifu) the values differ in every table, while for
01 (Hokkaido) and 22 to 47 they are the same; for example the two versions of Aomori
(02) have mesh codes that exist in only one of them. In the three prefectures compared by
hand (02, 13 and 22) the prefecture's total population is the same in both versions, which
suggests the difference is in how people are assigned to meshes, but the cause is not
confirmed. Do not merge the two versions; choose one and keep to it. Tables `T0011xx`
below `T001140` are JGD2000, those from `T001140` on are JGD2011 (the table name says which).

## Layout

```
raw/{f["run"]}/MANIFEST.json                 url, size, sha256, fetch time and row count of every file
raw/{f["run"]}/S/<table>/tbl<table>S<pref>.zip   {f["files"]} files, {f["bytes"] / 1e6:.0f} MB, exactly as e-Stat serves them
parquet/<table>.parquet                      one file per table, 47 prefectures each
parquet/columns.json                         each table's name, datum and the label of every column
```

The raw files are zips of one cp932 CSV each: a header line of column ids, a line of
Japanese column labels, then one row per mesh. `KEY_CODE` is the 8-digit mesh code.
`HTKSYORI`, `HTKSAKI` and `GASSAN` are the source's flags; in the files, `HTKSYORI` is
`0` for most rows and `2` for rows that carry the code of another mesh in `HTKSAKI`, which
looks like the mesh the row was merged into (this reading is from the files, not from
e-Stat's documentation). A value of `*` is a hidden value. The Parquet files hold the same
cells as strings (nothing is converted, so `*` is kept), with a `prefecture` column (the
two-digit code) in front.

| table | datum | name | columns | rows |
|---|---|---|---|---|
{tables}

## Licence

e-Stat's terms of use ({TERMS}) allow copying, redistribution and adaptation, including for
commercial use, on condition of the credit above and a note when the data has been
processed. The terms are compatible with CC BY 4.0, and the statistical GIS terms
({GIS_TERMS}, article 6) apply the same terms to the data it provides. This dataset is
therefore marked CC BY 4.0. The terms add that the government takes no responsibility for what
is done with the data, and that content may be changed or deleted without notice.

Collection code: <https://github.com/yuiseki/estat-census-mesh-2020> (MIT).
"""


def provenance(f: dict) -> str:
    return f"""source: 政府統計の総合窓口 (e-Stat) 統計GIS, 令和2年国勢調査, 3次メッシュ (1km)
url: {PAGE}
retrieved: {f["fetched"]}
run: {f["run"]}
terms: {TERMS}
files: {f["files"]}
rows: {f["rows"]}
"""


def main() -> int:
    f = facts()
    (DATA / "README.md").write_text(card(f), encoding="utf-8")
    (DATA / "provenance.yaml").write_text(provenance(f), encoding="utf-8")
    (DATA / "LICENSE").write_text(
        "Creative Commons Attribution 4.0 International (CC BY 4.0)\n"
        f"{CC}\n\n"
        "The data is the 2020 census grid-square statistics published by the Statistics Bureau\n"
        "of Japan through e-Stat. Credit: 政府統計の総合窓口(e-Stat) (https://www.e-stat.go.jp/),\n"
        "「令和2年国勢調査」(総務省統計局). The Parquet files are processed from the source:\n"
        "「令和2年国勢調査」(総務省統計局) を加工して作成.\n"
        f"e-Stat terms: {TERMS}\n",
        encoding="utf-8",
    )
    print(f"wrote data/README.md, LICENSE, provenance.yaml for run {f['run']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
