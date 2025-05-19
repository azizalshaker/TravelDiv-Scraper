import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}
url = "https://www.traveldiv.com/category/saudi-arabia/"
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

articles = soup.find_all("h2", class_="entry-title")

data = []
for article in articles:
    title = article.text.strip()
    link = article.find("a")["href"]

    article_resp = requests.get(link, headers=headers)
    article_soup = BeautifulSoup(article_resp.content, "html.parser")
    meta_desc = article_soup.find("meta", attrs={"name": "description"})
    description = meta_desc["content"] if meta_desc else "—"

    data.append({
        "العنوان": title,
        "الرابط": link,
        "الوصف": description
    })

df = pd.DataFrame(data)
df.to_csv("traveldiv_data.csv", index=False)
print("✅ تم حفظ البيانات في ملف traveldiv_data.csv")
