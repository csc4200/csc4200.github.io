import urllib.request

def fetch_page(url):
  with urllib.request.urlopen(url) as response:
    html = response.read()
  return html


if __name__ == '__main__':
    page = fetch_page("http://google.com")
    print(page)



