import requests

link = 'https://edu.pedmarkaz.uz/course/view.php?id=32'
link1 = 'https://edu.pedmarkaz.uz/lib/requirejs.php/1698645977/'
link3 = 'https://edu.pedmarkaz.uz/lib/javascript.php/1698645977/lib/requirejs/require.js'
link2 = 'https://edu.pedmarkaz.uz/pluginfile.php/19857/mod_folder/content/0/1.%20Talim%20jarayonidagi%20AKT/1-mavzu.%20Talim%20jarayonida%20axborot-kommunikatsiya%20texnologiyalari.docx?forcedownload=1'

response = requests.get(link1)
print(response.text)
# with open("download.html", "wb") as htmlFile:
#     htmlFile.write(response.content)
#     print('Download completed.')
