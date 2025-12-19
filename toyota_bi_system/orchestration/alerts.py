import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime

def send_error_email(context):
    """
    Function to be called when a DAG/Task fails.
    Sends email notification to the administrator.
    """
    # Ambil detail error dari context Airflow
    task_instance = context.get('task_instance')
    task_id = task_instance.task_id
    dag_id = task_instance.dag_id
    log_url = task_instance.log_url
    execution_date = context.get('execution_date')
    exception = context.get('exception')

    # Konfigurasi Pengirim dan Penerima
    sender_email = os.getenv('AIRFLOW__SMTP__SMTP_USER')
    sender_password = os.getenv('AIRFLOW__SMTP__SMTP_PASSWORD')
    receiver_email = "rifkyputram70@gmail.com"

    if not sender_password or "xxxx" in sender_password:
        print("[WARNING] Email password not configured. Skipping notification.")
        return

    subject = f"[ALERT] Disaster/Error Detected in DAG: {dag_id}"
    
    body = f"""
    <html>
      <body>
        <h2>🚨 SYSTEM FAILURE ALERT</h2>
        <p>A critical error has occurred in the Data Warehouse Pipeline.</p>
        <hr>
        <ul>
            <li><strong>DAG ID:</strong> {dag_id}</li>
            <li><strong>Task ID:</strong> {task_id}</li>
            <li><strong>Time:</strong> {execution_date}</li>
            <li><strong>Error:</strong> {str(exception)}</li>
        </ul>
        <p>Please check the logs immediately to prevent data loss.</p>
        <p><a href="{log_url}">Click here to view Logs</a></p>
        <hr>
        <p><em>Toyota BI Monitoring System</em></p>
      </body>
    </html>
    """

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    try:
        # Connect to Gmail SMTP Server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print(f"[SUCCESS] Alert email sent to {receiver_email}")
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")