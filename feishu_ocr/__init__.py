"""
飞书文档OCR处理工具

将飞书文档照片转制为Markdown文件。
"""

__version__ = "1.0.0"

from .engine import FeishuOCREngine

__all__ = ["FeishuOCREngine"]
