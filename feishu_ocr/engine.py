"""
飞书文档OCR识别引擎

基于RapidOCR，支持中英文混合识别，按y坐标排序输出。
"""

import os
from pathlib import Path
from typing import List, Dict, Tuple

try:
    from rapidocr_onnxruntime import RapidOCR
except ImportError:
    raise ImportError("请安装rapidocr-onnxruntime: pip install rapidocr-onnxruntime")


class FeishuOCREngine:
    """飞书文档OCR引擎
    
    Args:
        debug: 是否启用调试模式
    """
    
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.engine = RapidOCR()
        
    def ocr_single_image(self, image_path: str) -> List[Dict]:
        """OCR识别单张图片
        
        Args:
            image_path: 图像文件路径
            
        Returns:
            OCR结果列表，每个元素包含 text, confidence, y_position
        """
        try:
            result, _ = self.engine(image_path)
            if not result:
                return []
            
            lines = []
            for box, text, confidence in result:
                y = (box[0][1] + box[2][1]) / 2
                try:
                    conf_float = float(confidence)
                except (ValueError, TypeError):
                    conf_float = 0.0
                lines.append({
                    "text": text,
                    "confidence": conf_float,
                    "y_position": y,
                    "box": box
                })
            
            lines.sort(key=lambda x: x["y_position"])
            return lines
        except Exception as e:
            if self.debug:
                print(f"OCR错误 ({image_path}): {e}")
            return []
    
    def extract_title(self, image_path: str) -> Tuple[str, float]:
        """从图片中提取文档标题
        
        Args:
            image_path: 图像文件路径
            
        Returns:
            (标题, 置信度) 元组
        """
        lines = self.ocr_single_image(image_path)
        if not lines:
            return "", 0.0
        
        for line in lines[:3]:
            text = line["text"].strip()
            confidence = line["confidence"]
            
            if len(text) < 2:
                continue
            if text.isdigit() or text.isascii():
                continue
            if any(kw in text for kw in ["公司秘密", "内部公开", "公司机密", "Secret", "Internal"]):
                continue
            if "feishu.cn" in text or "http" in text:
                continue
            return text, confidence
        
        for line in lines:
            text = line["text"].strip()
            if len(text) >= 2:
                return text, line["confidence"]
        return "", 0.0
    
    def get_all_photos(self, image_dir: str, prefix: str = "Z30_", start_idx: int = 1532, end_idx: int = 2973) -> List[str]:
        """获取目录中的所有照片路径
        
        Args:
            image_dir: 图像目录
            prefix: 文件名前缀
            start_idx: 起始索引
            end_idx: 结束索引
            
        Returns:
            照片路径列表
        """
        photos = []
        for idx in range(start_idx, end_idx + 1):
            photo_path = os.path.join(image_dir, f"{prefix}{idx}.JPG")
            if os.path.exists(photo_path):
                photos.append(photo_path)
        return photos
