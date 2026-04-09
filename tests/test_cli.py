from pathlib import Path
import subprocess
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
# 这些测试通过真实子进程调用 CLI，更接近用户实际使用方式。


def write_csv(path, content):
    # 统一生成临时 CSV，减少重复样板代码。
    path.write_text(content, encoding="utf-8")


def run_cli(*args, cwd=None):
    # 捕获标准输出和标准错误，便于同时断言退出码和提示信息。
    return subprocess.run(
        [sys.executable, "-m", "chemical_visualizer.cli", *args],
        cwd=str(cwd or REPO_ROOT),
        capture_output=True,
        text=True,
    )


def test_cli_generates_outputs(tmp_path):
    # 成功路径：应生成 Excel 和两张 PNG。
    csv_path = tmp_path / "input.csv"
    image_dir = tmp_path / "images"
    excel_path = tmp_path / "result.xlsx"
    write_csv(csv_path, "Index,SMILES\n1,CCO\n2,CCN\n")

    result = run_cli(str(csv_path), "-o", str(excel_path), "-i", str(image_dir), "-s", "240x180")

    assert result.returncode == 0, result.stderr
    assert "Loaded 2 compounds" in result.stdout
    assert "Processed: 2 successful, 0 failed" in result.stdout
    assert excel_path.exists()
    assert image_dir.exists()
    assert len(list(image_dir.glob("*.png"))) == 2


def test_cli_reports_missing_file(tmp_path):
    # 常见错误路径：输入文件不存在。
    missing_path = tmp_path / "missing.csv"

    result = run_cli(str(missing_path))

    assert result.returncode == 1
    assert "File not found" in result.stderr


def test_cli_rejects_invalid_image_size(tmp_path):
    # 参数错误应在 argparse 阶段直接返回错误码 2。
    csv_path = tmp_path / "input.csv"
    write_csv(csv_path, "Index,SMILES\n1,CCO\n")

    result = run_cli(str(csv_path), "-s", "wide")

    assert result.returncode == 2
    assert "Image size must be in WxH format" in result.stderr
