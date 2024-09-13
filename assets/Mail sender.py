import time
import brevo
from brevo import ApiClient
from brevo.model.send_smtp_email import SendSmtpEmail
from brevo.api.smtp_api import SMTPApi
from brevo.exceptions import ApiException
from faker import Faker

# Initialize the API client with your Brevo (Sendinblue) API key
configuration = brevo.Configuration()
configuration.api_key['api-key'] = 'YOUR_API_KEY'  # Replace with your actual API key

# Create an instance of the SMTP API
api_instance = SMTPApi(ApiClient(configuration))

# Initialize the Faker object for generating fake Muslim names
fake = Faker()

def generate_fake_muslim_name():
    """Generate a fake Muslim name."""
    return fake.first_name_male() + " " + fake.last_name()

def send_email(to_email, subject, content):
    """Send the email using Brevo API."""
    email = SendSmtpEmail(
        to=[{"email": to_email}],
        subject=subject,
        html_content=f"<html><body>{content}</body></html>"
    )

    try:
        api_response = api_instance.send_transac_email(email)
        print(f"Email sent to {to_email}, Response: {api_response}")
    except ApiException as e:
        print(f"Error sending email to {to_email}: {e}")

def load_recipients(filename):
    """Load recipients from a text file."""
    with open(filename, "r") as file:
        return [line.strip() for line in file if line.strip()]

# Load recipients from the text file
recipients = load_recipients("recipients.txt")

# Content template for the email
content_template = """
In response to the public notification in context to Waqf Amendment Bill 2024, I strongly suggest it to be rolled back for the following reasons listed below:

1. The Bill is maliciously designed to target the Muslim Community and to usurp or destroy the Waqf properties. The Bill was framed without consulting the Stakeholders (Muslims).

2. The concept of Waqf emerges from Islamic religious belief where a Waqif dedicates his/her self-acquired or inherited private property in the name of God for charitable purposes. However, the proposed Bill seeks to dismantle the salient features of the meticulously developed centuries-old waqf.

3. The role and powers given to the Collector as per the proposed Bill in the administration of Waqf properties is highly objectionable, as if the Collector will virtually take over the whole Waqf Administration, against the Waqf Board and Central Waqf Council. 

As per the proposed Bill, the Collector can re-open any waqf, even old and notified waqfs, and determine whether the property is government property or not. These provisions are autocratic and highly unsecular.

4. The Bill aims to dismantle the concept of Waqf by user, which is the essence of Waqf jurisprudence, endangering mosques, dargahs, and Qabrastans. The deletion of Waqf by user is also unconstitutional.

5. The Bill authorizes the government to nominate members to the Waqf board and amend the constitution of the Central Waqf Council, allowing non-Muslim members. This is undemocratic and discriminatory.

6. The deletion of protection from the Limitation Act is also discriminatory. Similar protection exists in the Hindu Endowment Act.

7. The curtailing of the powers of the Waqf Tribunal is also discriminatory.

8. The proposed amendments violate Articles 25, 26, 29, and 14 of the Indian Constitution.

Yours sincerely,
{name}
"""

# Loop through each recipient and send an email with a 5-second delay
for recipient in recipients:
    # Generate a fake Muslim name for the subject and content
    fake_name = generate_fake_muslim_name()
    
    # Prepare the subject and content with the generated name
    subject = f"I, {fake_name}, Reject Waqf Amendment Bill 2024"
    content = content_template.format(name=fake_name)
    
    # Send the email
    send_email(recipient, subject, content)
    
    # Wait for 5 seconds before sending the next email
    print(f"Waiting for 5 seconds before sending the next email...")
    time.sleep(5)
