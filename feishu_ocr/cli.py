"""
命令行接口
"""

import argparse
import sys
from typing import Optional

from . import __version__


def create_parser() -> argparse.ArgumentParser:
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        prog="feishu-ocr",
        description="飞书文档OCR处理工具 - 将飞书文档照片转制为Markdown文件"
    )
    parser.add_argument("--version", "-v", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--debug", "-d", action="store_true", help="调试模式")
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # ocr 命令
    ocr_parser = subparsers.add_parser("ocr", help="OCR识别单张图片或批量识别")
    ocr_parser.add_argument("input", help="输入图像路径或目录")
    ocr_parser.add_argument("--output", "-o", help="输出文件路径")
    ocr_parser.add_argument("--start-idx", type=int, default=1532, help="起始索引")
    ocr_parser.add_argument("--end-idx", type=int, default=2973, help="结束索引")
    
    # batch 命令
    batch_parser = subparsers.add_parser("batch", help="批量处理")
    batch_parser.add_argument("image_dir", help="图像目录")
    batch_parser.add_argument("--output", "-o", default="output", help="输出目录")
    batch_parser.add_argument("--batch-size", type=int, default=10, help="每批处理数量")
    batch_parser.add_argument("--resume", "-r", action="store_true", help="从断点继续")
    
    return parser


def cmd_ocr(args: argparse.Namespace) -> int:
    """OCR命令处理"""
    from pathlib import Path
    from .engine import FeishuOCREngine
    
    engine = FeishuOCREngine(debug=args.debug)
    input_path = Path(args.input)
    
    if input_path.is_file():
        title, confidence = engine.extract_title(str(input_path))
        print(f"文件: {input_path.name}")
        print(f"标题: {title}")
        print(f"置信度: {confidence:.2f}")
        
        lines = engine.ocr_single_image(str(input_path))
        print(f"\nOCR结果 ({len(lines)} 行):")
        for line in lines:
            print(f"  [{line['confidence']:.2f}] {line['text']}")
    elif input_path.is_dir():
        photos = engine.get_all_photos(str(input_path), start_idx=args.start_idx, end_idx=args.end_idx)
        print(f"找到 {len(photos)} 张照片")
    else:
        print(f"路径不存在: {input_path}")
        return 1
    return 0


def main(args: Optional[list] = None) -> int:
    """主函数"""
    parser = create_parser()
    parsed_args = parser.parse_args(args)
    
    if parsed_args.command is None:
        parser.print_help()
        return 0
    
    commands = {"ocr": cmd_ocr}
    handler = commands.get(parsed_args.command)
    
    if handler is None:
        print(f"命令开发中: {parsed_args.command}")
        return 0
    
    try:
        return handler(parsed_args)
    except KeyboardInterrupt:
        print("\n操作已取消")
        return 130
    except Exception as e:
        print(f"错误: {e}")
        if parsed_args.debug:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
