"""OCR引擎测试"""

import pytest
from pathlib import Path

from feishu_ocr.engine import FeishuOCREngine


class TestFeishuOCREngine:
    """OCR引擎测试类"""
    
    def test_init(self):
        """测试初始化"""
        engine = FeishuOCREngine(debug=False)
        assert engine.debug is False
        assert engine.engine is not None
    
    def test_init_debug(self):
        """测试调试模式初始化"""
        engine = FeishuOCREngine(debug=True)
        assert engine.debug is True
    
    def test_ocr_single_image_no_file(self, tmp_path):
        """测试OCR识别不存在的文件"""
        engine = FeishuOCREngine()
        non_existent = str(tmp_path / "non_existent.JPG")
        lines = engine.ocr_single_image(non_existent)
        assert lines == []
    
    def test_extract_title_no_file(self, tmp_path):
        """测试从不存在的文件提取标题"""
        engine = FeishuOCREngine()
        non_existent = str(tmp_path / "non_existent.JPG")
        title, confidence = engine.extract_title(non_existent)
        assert title == ""
        assert confidence == 0.0
    
    def test_get_all_photos_empty_dir(self, tmp_path):
        """测试获取空目录的照片"""
        engine = FeishuOCREngine()
        photos = engine.get_all_photos(str(tmp_path))
        assert photos == []


if __name__ == "__main__":
    pytest.main([__file__])
