---
license: cc-by-4.0
license_name: cc-by-4.0
license_link: https://creativecommons.org/licenses/by/4.0/legalcode.ja
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
statistical GIS. 12 tables x 47 prefectures = 564 files, 2,134,320
rows, fetched on 2026-10-11 (the source lists them as updated 2025-10-09).

Source: 政府統計の総合窓口 (e-Stat) 地図で見る統計 (統計GIS), <https://www.e-stat.go.jp/gis/statmap-search?page=1&type=1&toukeiCode=00200521&toukeiYear=2020&aggregateUnit=S&serveyId=S002005112020&statsId=T001100>.

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
raw/2026-10-11/MANIFEST.json                 url, size, sha256, fetch time and row count of every file
raw/2026-10-11/S/<table>/tbl<table>S<pref>.zip   564 files, 116 MB, exactly as e-Stat serves them
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
| `T001100` | JGD2000 | 人口及び世帯 （JGD2000） | 54 | 177,859 |
| `T001107` | JGD2000 | 人口移動、就業状態等及び従業地・通学地 （JGD2000） | 98 | 177,859 |
| `T001140` | JGD2011 | 人口及び世帯 （JGD2011） | 54 | 177,861 |
| `T001143` | JGD2011 | 人口移動、就業状態等及び従業地・通学地 （JGD2011） | 98 | 177,861 |
| `T001171` | JGD2000 | ５歳階級別人口（JGD2000） | 69 | 177,859 |
| `T001179` | JGD2000 | 労働力状態、産業分類及び職業分類別人口（１５歳以上）（JGD2000） | 115 | 177,859 |
| `T001180` | JGD2000 | 住宅の所有及び建て方（JGD2000） | 25 | 177,859 |
| `T001181` | JGD2000 | ５年前の常住地及び従業地・通学地等（JGD2000） | 124 | 177,859 |
| `T001188` | JGD2011 | ５歳階級別人口（JGD2011） | 69 | 177,861 |
| `T001189` | JGD2011 | 労働力状態、産業分類及び職業分類別人口（１５歳以上）（JGD2011） | 115 | 177,861 |
| `T001190` | JGD2011 | 住宅の所有及び建て方（JGD2011） | 25 | 177,861 |
| `T001191` | JGD2011 | ５年前の常住地及び従業地・通学地等（JGD2011） | 124 | 177,861 |

## Licence

e-Stat's terms of use (https://www.e-stat.go.jp/terms-of-use) allow copying, redistribution and adaptation, including for
commercial use, on condition of the credit above and a note when the data has been
processed. The terms are compatible with CC BY 4.0, and the statistical GIS terms
(https://www.e-stat.go.jp/gis-terms, article 6) apply the same terms to the data it provides. This dataset is
therefore marked CC BY 4.0. The terms add that the government takes no responsibility for what
is done with the data, and that content may be changed or deleted without notice.

Collection code: <https://github.com/yuiseki/estat-census-mesh-2020> (MIT).
