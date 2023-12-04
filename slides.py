import os
import sys

notebook = sys.argv[1]
flag = len(sys.argv)==3

with open(f"notebooks\{notebook}.ipynb", 'r') as f:
      contents = f.read()
      updated = contents.replace(
            '"metadata": {}',
            '"metadata": {"slideshow": {"slide_type": "slide"}}'
        )
with open(f"notebooks\{notebook}.ipynb", 'w') as f:
      f.write(updated)
os.system(f'jupyter nbconvert notebooks\{notebook}.ipynb --to slides --SlidesExporter.reveal_scroll=True')
os.system(f"move notebooks\{notebook}.slides.html docs\{notebook}.slides.html")
if flag:
    os.system(f'decktape automatic docs\{notebook}.slides.html docs\pdfs\{notebook}.slides.pdf')