# Feishu Document OCR Tool

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Convert Feishu (Lark) document photos into Markdown files that can be directly pasted into Feishu.

## Features

- 🔍 **OCR Recognition**: Based on RapidOCR, supports mixed Chinese and English text recognition
- 📄 **Document Segmentation**: Automatically detects new document boundaries by title changes
- 🔗 **Continuation Merging**: Automatically identifies and merges continuation documents
- ✅ **Quality Check**: Line-by-line comparison to ensure content consistency
- 📦 **Batch Processing**: Supports resuming from breakpoints

## Installation

```bash
pip install git+https://github.com/ikownive/Feishu_doc_photo_OCR_md.git
```

## Usage

### Command Line

```bash
# Single image OCR
feishu-ocr ocr image.JPG

# Batch processing
feishu-ocr batch images/ --output output/

# Document segmentation
feishu-ocr segment images/ --output segments.json

# Quality check
feishu-ocr check doc.md --photos photo1.JPG photo2.JPG
```

### Python API

```python
from feishu_ocr import FeishuOCREngine

engine = FeishuOCREngine()
title, confidence = engine.extract_title("image.JPG")
lines = engine.ocr_single_image("image.JPG")
```

## Dependencies

- Python >= 3.8
- rapidocr-onnxruntime >= 1.3.0

## License

MIT License
