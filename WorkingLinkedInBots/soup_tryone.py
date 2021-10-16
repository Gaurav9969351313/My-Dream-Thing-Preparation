import re
from requests_html import HTMLSession

url = 'https://www.google.com/search?q=%22Germany%22+%22Email%22+AND+%22Headhunter%22+site:linkedin.com&start=30'
EMAIL_REGEX = r"[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+"

session = HTMLSession()

r = session.get(url)

r.html.render()
for re_match in re.finditer(EMAIL_REGEX, r.html.raw_html.decode()):
    print(re_match.group())
