import sys
import os
import subprocess

# 필요한 패키지 목록
REQUIRED_PACKAGES = ["nbformat", "nbconvert"]

# 패키지 자동 설치 함수
def install_missing_packages():
    for package in REQUIRED_PACKAGES:
        try:
            __import__(package)
        except ModuleNotFoundError:
            print(f"Installing missing package: {package}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

import sys
import os
import nbformat
from nbconvert import HTMLExporter

def convert_notebook_to_html(ipynb_path):
    """Jupyter Notebook을 HTML로 변환 (내부 스타일 제거)"""
    with open(ipynb_path, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, as_version=4)

    # nbconvert 기본 CSS 포함하지 않도록 설정
    html_exporter = HTMLExporter(template_name="basic")  # 기본 템플릿 사용 (Jupyter 스타일 제거)
    html_exporter.exclude_input_prompt = True  # 입력 프롬프트 제거
    html_exporter.exclude_output_prompt = True  # 출력 프롬프트 제거
    html_exporter.exclude_raw = True  # raw cell 제외

    notebook_html, _ = html_exporter.from_notebook_node(notebook)

    # 최종 HTML 생성 (외부 CSS 포함)
    output_html = f"""
<div class="jupyter-container p-0 m-0">{notebook_html}</div>
""" 

    return output_html

pass

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: python convert_ipynb.py <notebook.ipynb>")
        sys.exit(1)

    ipynb_path = sys.argv[1]

    if not os.path.exists(ipynb_path):
        print(f"Error: File '{ipynb_path}' not found.")
        sys.exit(1)

    output_html = convert_notebook_to_html(ipynb_path)
    
    print( output_html )

pass
