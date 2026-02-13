"""
金融行情简报发布技能打包脚本
将技能目录打包为 .skill 文件（实际为zip格式）
"""

import os
import zipfile
from pathlib import Path

def create_skill_package(skill_dir, output_dir=None):
    """
    打包技能目录为.skill文件
    
    Args:
        skill_dir: 技能目录路径
        output_dir: 输出目录（可选）
    """
    skill_path = Path(skill_dir)
    skill_name = skill_path.name
    
    # 确定输出路径
    if output_dir:
        output_path = Path(output_dir)
    else:
        output_path = skill_path.parent
    
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 创建.skill文件（zip格式）
    skill_file = output_path / f"{skill_name}.skill"
    
    print(f"正在打包技能: {skill_name}")
    print(f"源目录: {skill_path}")
    print(f"输出文件: {skill_file}")
    
    with zipfile.ZipFile(skill_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(skill_path):
            for file in files:
                file_path = Path(root) / file
                # 计算相对路径
                arcname = file_path.relative_to(skill_path.parent)
                print(f"  添加: {arcname}")
                zipf.write(file_path, arcname)
    
    print(f"\n✓ 技能打包完成: {skill_file}")
    print(f"  文件大小: {skill_file.stat().st_size / 1024:.2f} KB")
    return skill_file

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python package_skill.py <skill_directory> [output_directory]")
        sys.exit(1)
    
    skill_dir = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        create_skill_package(skill_dir, output_dir)
    except Exception as e:
        print(f"✗ 打包失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
