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
      fromaddr = "tejalsarode2810@gmail.com"
      from_add_password= "bcwtznoizyxogvlf"
      toaddr = to_add

      email_subject="Java Developer - Resume: Tejal Sarode"
      resume_path="./Resume-TejalSarode-JavaDeveloper.pdf"
      filename = "Resume-TejalSarode-JavaDeveloper.pdf"

      msg = MIMEMultipart('alternative')
      msg['From'] = fromaddr
      msg['To'] = toaddr
      msg['Subject'] = email_subject

      body = "Dear Hiring Manager, Please find attached resume."

      text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
      html = """
        <html>
  <head></head>
  <body style=" font-family: Arial, Helvetica, sans-serif; font-size: 22px">
    
    <h4>Dear Hiring Manager,</h4> 
    <h6>I hope you are doing well. <h6>

    <p style="font-weight: normal; line-height: 24px">
    	I am writing to express my strong interest in being the next Full Stack Developer at your organisation.
	    <br>
	    As an ambitious professional and having dream of <span style="font-size: 16px; font-weight:bold"> aspiring Java Developer.</span> I have learnt  <span style="font-size: 16px; font-weight:bold">Core Java, Spring Boot, Rest API, Oracle, Git and agile.</span> 
		I believe that I would make an excellent addition to your team.
		<br>
		<br>
		I have attached my CV hoping that you will consider me for the place in your organisation, should you need more details or references I can supply those at your convenience. Otherwise I would like to have an interview and talk more about being new employee for your esteemed Organisation. Please review.

		<br>
		<br>
		Thank you so much for your time and consideration..:)
		<br>
	</p>

	<table style="font-weight: normal; line-height: 24px;" border=1>
	
		<tr>
			<td style="font-weight: bold;">Location Preferences</td>
			<td>Mumbai, Pune</td>
		</tr>
		<tr>
			<td style="font-weight: bold;">Notice Period</td>
			<td>10 Days</td>
		</tr>
	</table>
	<br>

	<p style="line-height: 24px">With Best Regards,<br></p>
	<p style="line-height: 22px; font-weight: normal;">	
		Mr. Tejal Sanjay Sarode. <br>
		[M]: tejalsarode2810@gmail.com<br>
		[H]: +91 9579676068.<br>
	</p>

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