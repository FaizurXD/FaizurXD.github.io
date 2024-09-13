import time
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from faker import Faker
from pprint import pprint

# Setup Faker for generating fake Muslim names
fake = Faker()

# Generate a fake Muslim name
def generate_fake_muslim_name():
    return fake.first_name_male() + " " + fake.last_name()

# Function to send email via Brevo's API
def send_email(recipient_email, sender_name, sender_email, subject, html_content):
    # Setup the Brevo API client
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = 'YOUR_API_V3_KEY'  # Replace with your actual Brevo API key

    # Create API instance
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    
    # Create the email content
    email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": recipient_email}],
        sender={"name": sender_name, "email": sender_email},
        subject=subject,
        html_content=html_content
    )

    try:
        # Send the email via Brevo API
        api_response = api_instance.send_transac_email(email)
        pprint(api_response)
    except ApiException as e:
        print(f"Exception when sending email to {recipient_email}: {e}")

# Function to send emails repeatedly with a delay
def send_emails_with_gap(recipient_email, sender_name, sender_email, base_subject, base_html_content, times, delay_seconds=5):
    for i in range(times):
        # Generate a fake Muslim name
        fake_name = generate_fake_muslim_name()

        # Create the subject and body with the generated name
        subject = base_subject.replace("{generate_fake_muslims_names}", fake_name)
        html_content = base_html_content.replace("{generate_fake_muslims_names}", fake_name)

        # Send the email
        send_email(recipient_email, sender_name, sender_email, subject, html_content)

        print(f"Email {i+1} sent to {recipient_email}. Waiting for {delay_seconds} seconds...")
        # Wait for the specified delay
        time.sleep(delay_seconds)

# Main block to execute email sending
if __name__ == "__main__":
    # Specify recipient email, sender details, and number of emails to send
    recipient_email = "recipient@example.com"  # Replace with the recipient's email
    sender_name = "Your Name"
    sender_email = "yourname@yourdomain.com"  # Replace with your sender email
    times_to_send = 10  # Number of times to send the email

    # Email subject and content template
    subject_template = "I, {generate_fake_muslims_names}, Reject Waqf Amendment Bill 2024"
    html_content_template = """
    <p>In response to the public notification in context to Waqf Amendment Bill 2024, I strongly suggest it to be rolled back for the following reasons listed below:</p>

    <ol>
        <li>The Bill is maliciously designed to target the Muslim Community and to usurp or destroy the Waqf properties. The Bill was framed without consulting the stakeholders (Muslims).</li>
        <li>The concept of Waqf emerges from Islamic religious belief where a Waqif dedicates his/her self-acquired or inherited private property in the name of God for charity purposes. However, the proposed Bill seeks to dismantle the salient features of the meticulously developed centuries-old Waqf.</li>
        <li>The role and powers given to the Collector as per the proposed Bill in the administration of Waqf properties are highly objectionable. It is as if the Collector will virtually take over the whole Waqf Administration against the Waqf board and Central Waqf Council.</li>
        <li>The Bill authorizes the government to nominate members to the Waqf board. The proposed changes seek to amend the constitution of the central Waqf council and the Waqf board by allowing a majority of non-Muslims. This is not only undemocratic but also discriminatory.</li>
        <li>The Bill violates the rights of Waqf properties and is unconstitutional as it interferes with the fundamental rights provided in Articles 25, 26, and 29 of the Indian Constitution.</li>
        <li>The provisions for deleting protection from the Limitation Act, curtailing powers of the Waqf Tribunal, and giving control to the government over the Waqf board are against democratic principles.</li>
        <li>There are several discriminatory clauses, such as the involvement of the Collector in Waqf matters, which are not applicable to Hindu Endowments under the Hindu Endowment Act.</li>
    </ol>

    <p>Yours sincerely,<br>{generate_fake_muslims_names}</p>
    """

    # Call the function to send emails
    send_emails_with_gap(recipient_email, sender_name, sender_email, subject_template, html_content_template, times_to_send, delay_seconds=5)
