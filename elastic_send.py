import os
import requests
from dotenv import load_dotenv
from apscheduler.schedulers.blocking import BlockingScheduler
import logging
from datetime import datetime

# Load the .env file
load_dotenv()

# Configure the log file, format, and the minimum log level to capture
logging.basicConfig(
    filename='app.log', 
    filemode='a', 
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

ELASTIC_API_KEY = os.getenv("ELASTIC_API_KEY")
email_batch_size = os.getenv("email_batch_size")
hour_send_email = os.getenv("hour_send_email")
minute_send_email = os.getenv("minute_send_email")

def get_unsent_email(email_batch_size):
		headers = {'Content-Type': "application/json", 'Accept': "application/json"}
		check_api = "http://68.183.189.171:9999/unsentEmail"
		# check_api = "http://127.0.0.1:5049/unsentEmail"
		jsondata = {"name":email_batch_size}
		data = requests.get(check_api,json=jsondata,headers=headers)
		if data.status_code != 200:
			print(data.status_code)
			print(data.reason)
		else:
			print("OK")
			json_object = data.json()
			return json_object

def update_sent_email(email_id):
		headers = {'Content-Type': "application/json", 'Accept': "application/json"}
		check_api = "http://68.183.189.171:9999/setSentEmail"
		# check_api = "http://127.0.0.1:5049/setSentEmail"
		jsondata = {"name":email_id}
		data = requests.get(check_api,json=jsondata,headers=headers)
		if data.status_code != 200:
			print(data.status_code)
			print(data.reason)
		else:
			print("update OK ",email_id)
			json_object = data.json()
			return json_object

def send_transactional_email(
	to_email: str, 
	subject: str, 
	html_body: str, 
	from_email: str
):
	api_key = os.getenv("ELASTIC_API_KEY")
	# api_key = "9A30507AB3AA59B1C137028B25EB7628340AE5214433096A88284AD378F0EB8C46CF21A27811CADCCB870AFCBC584E8C"
	url = "https://api.elasticemail.com/v4/emails/transactional"
	
	headers = {
		"X-ElasticEmail-ApiKey": api_key,
		"Content-Type": "application/json"
	}
	# if isinstance(to_email, str):
	# 	to_email = [to_email]

	payload = {
  "Recipients": {
	"To": [to_email]
  },
  "Content": {
	"Body": [
	  {
		"ContentType": "HTML",
		"Content": html_body
	  },
	  {
		"ContentType": "PlainText",
		"Content": "Hello,\n\nYour verification code for Fitech is 129056. This code will expire in 10 minutes.\n\nBest regards,\nFitech Team"
	  }
	],
	"Subject": "Your Fitech Account Verification Code",
	"From": from_email
  }
}
	# payload = {
	#     "Recipients": {
	#         "To": [to_email]
	#     },
	#     "Content": {
	#         "Body": [
	#             {
	#                 "ContentType": "HTML",
	#                 "Content": html_body
	#             }
	#         ],
	#         "Subject": subject,
	#         "From": from_email
	#     }
	# }

	response = requests.post(url, headers=headers, json=payload)
	print(response)
	if response.status_code in (200, 202):
		print("Email sent successfully!")
		return response.status_code
		
	print(f"Failed to send email. Status Code: {response.status_code}")
	print(f"Response: {response.text}")
	return -1


def send_email():
	logging.info("Start to sent email")
	email_list = get_unsent_email(email_batch_size)
	email_str = ""
	for item in email_list:
		email_str +=  "\"" + item["email"] + "\"" + ","
	emails = email_str[:-1]
	send_status = -1
	if(email_str != ""):
		send_status = send_transactional_email(
		to_email = emails,
	    # to_email=["hatrankid@gmail.com","tran.habk0605@gmail.com","thuydt@fitech.com.vn"],
	    subject="Welcome to Our App!",
	    html_body="<p>Hello,</p><p>Your verification code for Fitech is <strong>129056</strong>. This code will expire in 10 minutes.</p><p>Best regards,<br>Fitech Team</p>",
	    from_email="hatn@fitech.com.vn"
	)
	if(send_status != -1):
		for item in email_list:
			update_sent_email(item["id"])
	logging.info("Send email successfully!")

# --- Example Usage ---
if __name__ == "__main__":
	scheduler = BlockingScheduler()

	# Option A: Run at 3 specific times of day (e.g., 8:00 AM, 1:00 PM, 6:00 PM)
	scheduler.add_job(send_email, 'cron', hour='2,10,18', minute=0)
	scheduler.add_job(send_email, 'cron', hour=hour_send_email, minute=minute_send_email)
	

	# Option B: Run every 8 hours interval
	# scheduler.add_job(send_email, 'interval', hours=8)
	scheduler.start()
	# # Ensure your API key is exported: export ELASTIC_EMAIL_API_KEY="your-key-here"
	# print("Starting to send email")
	# email_list = get_unsent_email(email_batch_size)
	# email_str = ""
	# for item in email_list:
	# 	email_str +=  "\"" + item["email"] + "\"" + ","
	# emails = email_str[:-1]
	# send_status = -1
	# if(email_str != ""):
	# 	send_status = send_transactional_email(
	# 	to_email = emails,
	#     # to_email=["hatrankid@gmail.com","tran.habk0605@gmail.com","thuydt@fitech.com.vn"],
	#     subject="Welcome to Our App!",
	#     html_body="<p>Hello,</p><p>Your verification code for Fitech is <strong>129056</strong>. This code will expire in 10 minutes.</p><p>Best regards,<br>Fitech Team</p>",
	#     from_email="hatn@fitech.com.vn"
	# )
	# if(send_status != -1):
	# 	for item in email_list:
	# 		update_sent_email(item["id"])