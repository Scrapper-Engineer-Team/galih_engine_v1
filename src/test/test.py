import requests

url = 'https://komisiyudisial.go.id/frontend/publication_download/62'

response = requests.get(url)
with open('test.pdf', 'wb') as f:
    f.write(response.content)
print('sukses!!!')