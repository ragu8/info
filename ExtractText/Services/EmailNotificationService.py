from typing import Optional
from boto3 import client

class EmailNotificationService:
    @staticmethod
    async def send_message(sns_client: client, file: str, sns_arn: str) -> Optional[dict]:
        try:
            message = (
                "Greetings!\r\n\r\nFollowing documents processed successfully :\r\n\r\n"
                f"{file}\r\n\r\n\r\nThank you\r\n\r\nTeam SIMS\r\n"
            )
            subject = f"SIMS: File Status - {file}"
            response = sns_client.publish(
                TopicArn=sns_arn,
                Subject=subject,
                Message=message
            )
            return response
        except Exception as e:
            print(f"Error occurred while sending message: {e}")
            return None

