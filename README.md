# Data Vis Decompiler

## Developmental Setup

### Pretrained Models

Pretrained models should be unzipped into `backend/marks`, structure should be something like,

```
backend/marks/
  box_model2/
    saved_model.pb
    assets/
    variables/
```

|Name|Link|
|----|-------------|
|`box_model`|[Download](https://www.dropbox.com/s/33xi78jockuvrsi/box_model.zip?dl=1)|
|`box_model2`|[Download](https://www.dropbox.com/s/aum7nifjmzhwlny/box_model2.zip?dl=1)|

### Running

Install Python Deps,

```
pip install -r requirements.txt
```

Unpack pretrained models as described in the next subsection.

Run dev server,

```
python serve.py
```

Inside `frontend/`, install deps,

```
npm install
```

And while the backend is running, finally,

```
npm run serve
```

Chrome extention launcher can be loaded as an unpacked web extention.

## Research Commentary

