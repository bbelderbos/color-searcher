from pathlib import Path
from urllib.request import urlretrieve

from rich.console import Console

console = Console()

colors_csv_url = "https://raw.githubusercontent.com/codebrainz/color-names/master/output/colors.csv"
colors_csv_file = Path(colors_csv_url).name

def download_data():
    console.print("Grabbing colors.csv from GitHub")
    urlretrieve(colors_csv_url, colors_csv_file)
    console.print("Adding header to the file")
    with open(colors_csv_file, 'r') as f:
        data = f.read()
    with open(colors_csv_file, 'w') as f:
        header = "name,name2,hex,r,g,b"
        f.write(f"{header}\n" + data)
