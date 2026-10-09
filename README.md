# PEEK Project Page

Static project page for **PEEK: One-Step-Look-Ahead Exposure Bias Correction for Diffusion Sampling**.

Public site: [wendybaiyunwei.github.io/PEEK-Video](https://wendybaiyunwei.github.io/PEEK-Video/)

## Local preview

From the repository root, run:

```bash
python -m http.server 8000
```

Then open `http://127.0.0.1:8000/`.

## Validation

The lightweight checks verify project links, local media assets, metadata, semantic landmarks, and accessible names:

```bash
python -m unittest discover -s tests -v
```

