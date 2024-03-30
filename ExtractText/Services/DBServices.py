import pymysql
from ExtractText.Models import DocumentStatus
from datetime import datetime

class DBServices:
    @staticmethod
    def insert_document_data(created_by: str, file_name: str, original_data_returned_by_api: str, connection_string: str, page_number: int, file_path: str, image_file_path: str, original_name: str) -> int:
        try:
            with pymysql.connect(**connection_string) as connection:
                cmd_text = "INSERT INTO `SIMS`.`sims_process_detail`(`Document Name`,`Original Data set returned by API`,`User ID`,`Updated Datetime`,`Original Document Name`,`Scanned Page Number`,`File Path`,`ImageFilePath`,`Reviewed/Edited Data set`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cmd_values = (file_name, original_data_returned_by_api, created_by, datetime.now(), original_name, page_number, file_path, image_file_path, '{}')
                with connection.cursor() as cursor:
                    cursor.execute(cmd_text, cmd_values)
                    connection.commit()
                    return cursor.rowcount
        except Exception as e:
            print(f"Error occurred while inserting document data: {e}")
            return 0

    @staticmethod
    def update_document_status(file_name: str, connection_string: str) -> int:
        try:
            with pymysql.connect(**connection_string) as connection:
                cmd_text = "UPDATE `SIMS`.`sims_document_status` SET `Document Status`=%s, `Updated Datetime`=%s, `Bucket`=%s, `IsMailSend`=%s WHERE `Document Orignal Name`=%s AND IsMailSend=0"
                cmd_values = ("Done", datetime.now(), "Completed", True, file_name)
                with connection.cursor() as cursor:
                    cursor.execute(cmd_text, cmd_values)
                    connection.commit()
                    return cursor.rowcount
        except Exception as e:
            print(f"Error occurred while updating document status: {e}")
            return 0

    @staticmethod
    def get_document_status(file_original_name: str, connection_string: str) -> DocumentStatus:
        document_status = DocumentStatus()
        try:
            with pymysql.connect(**connection_string) as connection:
                cmd_text = "SELECT * FROM SIMS.sims_document_status WHERE `Document Name` = %s AND IsMailSend=0 ORDER BY PageNumber LIMIT 1"
                with connection.cursor() as cursor:
                    cursor.execute(cmd_text, (file_original_name,))
                    result = cursor.fetchone()
                    if result:
                        document_status.DocumentName = result["Document Orignal Name"]
                        document_status.CreatedBy = result["CreatedBy"]
                        document_status.PageNumber = result["PageNumber"]
                        document_status.IsMailSend = bool(result["IsMailSend"])
                        document_status.IsLastPage = bool(result["IsLastPage"])
        except Exception as e:
            print(f"Error occurred while fetching document status: {e}")
        return document_status

