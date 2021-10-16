import smtplib
import openpyxl
from ipython_genutils.py3compat import xrange
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# https://myaccount.google.com/lesssecureapps

wb = openpyxl.load_workbook('./EmailData.xlsx')
worksheet = wb.get_sheet_by_name("Test")
first_column = worksheet['A']

for x in xrange(len(first_column)):
    if first_column[x].value != "email":
      print(first_column[x].value)
      to_add = first_column[x].value 
      fromaddr = "gauravtalele2021@gmail.com"
      from_add_password= "gauravtalele*123"
      toaddr = to_add

      email_subject="Sr. Full Stack Develoer (Resume - Gaurav Talele)"
      resume_path="./Resume - Gaurav Talele.pdf"
      filename = "Resume - Gaurav Talele.pdf"

      msg = MIMEMultipart('alternative')
      msg['From'] = fromaddr
      msg['To'] = toaddr
      msg['Subject'] = email_subject

      body = "Dear Hiring Manager, Please find attached resume."

      text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
      html = """\
      <html>
        <head></head>
        <body>
          
          <h4>Dear Hiring Manager,</h4> 
          <h6>I hope you’re doing well. <h6>

          I am writing to express my strong interest in being the next Full Stack Engineer at your organisation.
          <br>
          As an ambitious professional with experience in Angular, Angular Material, Spring Boot, Core Java, Microservices, Axon, Oracle, MongoDB, Jasper Reports,
      Docker, Docker Compose, AWS. I believe that I would make an excellent addition to your team. I am currently working as a Full Stack Engineer in 
      Reserve Bank Of Information Technologies Pvt Ltd.
      <br>
      <br>
      I have attached my CV hoping that you will consider me for the place in your organisation, should you need more details or references I can supply those at your convenience. Otherwise I would like to have an interview and talk more about being new employee for your esteemed Organisation. Please review.

      <br>
      <br>
      Thank you so much for your time and consideration..:)
      <br>

      <p>Current CTC: 12.76 LPA<p>
      <p>Notice Period: 45 days.</p>

      <p>Also It would be great if you foreword me the detailed JD.</p>
      <br>
      <br>

      With Best Regards,<br>
      Mr. Gaurav Y Talele. <br>
      [M]: garry.talele@gmail.com<br>
      [H]: +91 9969351313.<br>
        </body>
      </html>
      """

      part1 = MIMEText(text, 'plain')
      part2 = MIMEText(html, 'html')
      msg.attach(part1)
      msg.attach(part2)

      attachment = open(resume_path, "rb")
      p = MIMEBase('application', 'octet-stream')

      p.set_payload((attachment).read())
      encoders.encode_base64(p)
      p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
      msg.attach(p)
      s = smtplib.SMTP('smtp.gmail.com', 587)
      s.starttls()

      s.login(fromaddr, from_add_password)
      text = msg.as_string()
      s.sendmail(fromaddr, toaddr, text)
      s.quit()