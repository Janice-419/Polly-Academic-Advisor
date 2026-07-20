import requests
from bs4 import BeautifulSoup

with open(
    "data/links/links.txt",
    "r",
    encoding="utf-8"
) as f:

    urls = f.readlines()

all_text = ""

for url in urls:

    url = url.strip()

    try:

        print("Reading:", url)

        response = requests.get(url)

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        text = soup.get_text()

        all_text += "\n\n"
        all_text += "=" * 50
        all_text += "\n"
        all_text += url
        all_text += "\n"
        all_text += text

    except Exception as e:

        print("Error:", e)

with open(
    "output/web_text.txt",
    "w",
    encoding="utf-8"
) as f:

    f.write(all_text)

print("Website extraction completed!")