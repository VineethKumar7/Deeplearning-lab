#!/usr/bin/env python3
import os
import nbformat
from nbconvert import MarkdownExporter
import markdown as md

def ConvertAllNotebooksToHtml(OutputFolderName="html_exports"):
    """
    1) Finds every .ipynb in the current directory
    2) Strips out Jupyter-Widget bundles
    3) Exports notebook content to Markdown
    4) Converts Markdown to HTML
    5) Writes each .html into OutputFolderName
    """
    cwd = os.getcwd()
    outDir = os.path.join(cwd, OutputFolderName)
    os.makedirs(outDir, exist_ok=True)

    # Set up the Markdown exporter
    mdExporter = MarkdownExporter()

    for fname in os.listdir(cwd):
        if not fname.endswith(".ipynb"):
            continue

        print(f"Converting {fname} → {OutputFolderName}/{fname[:-6]}.html…")
        nbPath = os.path.join(cwd, fname)
        nb = nbformat.read(nbPath, as_version=4)

        # 1) Strip any widget metadata & outputs entirely
        for cell in nb.cells:
            cell.metadata.pop("widgets", None)
            if "outputs" in cell:
                cell.outputs = [
                    out for out in cell.outputs
                    if not any(
                        k.startswith("application/vnd.jupyter.widget") 
                        for k in out.get("data", {})
                    )
                ]

        # 2) Export to Markdown
        (markdownBody, resources) = mdExporter.from_notebook_node(nb)

        # 3) Convert Markdown → HTML
        htmlBody = md.markdown(
            markdownBody,
            extensions=["fenced_code", "tables", "codehilite"]
        )

        # 4) Wrap in a basic HTML scaffold
        fullHtml = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8"/>
  <title>{fname}</title>
</head>
<body>
{htmlBody}
</body>
</html>"""

        # 5) Write out the HTML
        outPath = os.path.join(outDir, f"{fname[:-6]}.html")
        with open(outPath, "w", encoding="utf-8") as f:
            f.write(fullHtml)

    print(f"\n✅ All done! HTML files are in ./{OutputFolderName}")

if __name__ == "__main__":
    # Ensure you have the 'markdown' package: pip install markdown
    ConvertAllNotebooksToHtml()
