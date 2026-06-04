#!/usr/bin/env python3
"""
基本使用示例
"""

from feishu_ocr import FeishuOCREngine


def main():
    """主函数"""
    print("飞书文档OCR处理工具 - 使用示例")
    print("=" * 40)
    
    # 初始化OCR引擎
    engine = FeishuOCREngine(debug=False)
    
    # 替换为实际图片路径
    image_path = "path/to/your/image.JPG"
    
    print(f"\n图片路径: {image_path}")
    print("请将路径替换为实际的图片文件路径")
    
    # 提取标题
    title, confidence = engine.extract_title(image_path)
    print(f"标题: {title}")
    print(f"置信度: {confidence:.2f}")
    
    # OCR识别所有内容
    lines = engine.ocr_single_image(image_path)
    print(f"\n识别到 {len(lines)} 行文本:")
    for i, line in enumerate(lines[:5], 1):
        print(f"  {i}. [{line['confidence']:.2f}] {line['text']}")
    
    if len(lines) > 5:
        print(f"  ... 还有 {len(lines) - 5} 行")


if __name__ == "__main__":
    main()
