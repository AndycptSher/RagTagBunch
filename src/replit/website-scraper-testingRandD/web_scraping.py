

import requests

websites = ["https://stonks.gg/margin", 'https://www.monster.com/jobs/search/?q=Software-Developer&where=Australia', "https://skyblock.matdoes.dev/bazaar/blaze_is_a_boomer", "https://sky.lea.moe/api/bazaar?html"]
for y, x in enumerate(websites):
  print(y, x, "\n")
page = requests.get(websites[int(input("which website?: "))])
print(page.text)
for x in page.text.split("<tr>"):
  print(x)