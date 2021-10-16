import pdfkit

# choco install wkhtmltopdf
# Env Path Variable c:\program files\wkhtmltopdf\bin\wkhtmltopdf.exe

url = 'http://127.0.0.1:5500/index.html'
pdfkit.from_url(url, 'Resume-GauravTalele.pdf')
# pdfkit.from_file('index.html', 'out.pdf')