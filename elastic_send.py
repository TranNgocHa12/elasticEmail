import os
import requests

def send_transactional_email(
    to_email: str, 
    subject: str, 
    html_body: str, 
    from_email: str
):
    # api_key = os.environ.get("ELASTIC_EMAIL_API_KEY")
    api_key = "9A30507AB3AA59B1C137028B25EB7628340AE5214433096A88284AD378F0EB8C46CF21A27811CADCCB870AFCBC584E8C"
    url = "https://api.elasticemail.com/v4/emails/transactional"
    
    headers = {
        "X-ElasticEmail-ApiKey": api_key,
        "Content-Type": "application/json"
    }
    if isinstance(to_email, str):
        to_email = [to_email]

    payload = {
  "Recipients": {
    "To": to_email
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
        return response.json()
        
    print(f"Failed to send email. Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    return None


# --- Example Usage ---
if __name__ == "__main__":
    # Ensure your API key is exported: export ELASTIC_EMAIL_API_KEY="your-key-here"
    send_transactional_email(
        to_email=["hatrankid@gmail.com","tran.habk0605@gmail.com","thuydt@fitech.com.vn"],
        subject="Welcome to Our App!",
        html_body="<p>Hello,</p><p>Your verification code for Fitech is <strong>129056</strong>. This code will expire in 10 minutes.</p><p>Best regards,<br>Fitech Team</p>",
        from_email="hatn@fitech.com.vn"
    )