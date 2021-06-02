# find-the-cheapest

## Installation

`pip install git+https://www.github.com/Smirkey/find-the-cheapest.git`

## Usage

```python
from leboncoin_selenium import run_sourcing, load_importer_exporter

importer, exporter = load_importer_exporter(
    mode='local', # s3 or local
    aws_access_key_id='',
    aws_secret_access_key='',
    aws_bucket='', # leboncoin_storage
    local_path=''
)

run_sourcing(
    importer,
    exporter,
    categories=['chaussures']
)
```

## Vinted Scrapy
```bash 
scrapy crawl vinted
```

#### Vinted categories table

|Id|Title|Item count|
|--|-----|----------|
|1904|Women|174277854|
|4|Clothes|133422995|
|1193|Kids|104463026|
|1195|Girls' clothing|50341093|
|12|Tops & t-shirts|39248886|
|1194|Boys' clothing|36668914|
|5|Men|26724199|
|10|Dresses |23040362|
|2050|Clothes|21495316|
|16|Shoes|18311080|
|13|Jumpers & sweaters|15216415|
|1037|Coats & jackets|13548552|
|1187|Accessories|13396688|
|1918|Home|11405149|
|1499|Toys & games|10664769|
|221|T-shirts|9583502|
|1245|Tops & t-shirts|9326605|
|1198|Tops & t-shirts|8793216|
|11|Skirts|8229277|
|1921|Books|8061621|

### Vinted countries table

|Id|Country|
|--|-----|
|16|France|
|19|Belgique|
|7|Espagne|
|20|Luxembourg|
|10|Pays-Bas|
|18|Italie|