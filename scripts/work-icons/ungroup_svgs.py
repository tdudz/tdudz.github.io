from pathlib import Path
import xml.etree.ElementTree as ET


SVG = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG)
ROOT = Path(__file__).resolve().parent

for path in (ROOT / "vectors").glob("*.svg"):
    tree = ET.parse(path)
    root = tree.getroot()
    for group in list(root.findall(f"{{{SVG}}}g")):
        transform = group.get("transform")
        for child in list(group):
            if transform:
                child.set("transform", transform)
            root.append(child)
        root.remove(group)
    tree.write(path, encoding="unicode", xml_declaration=True)
