import boto3
from io import BytesIO
import json
from typing import Dict, List
from boto3.session import Session
from botocore.exceptions import ClientError
from PIL import Image

class AWSTextractService:
    @staticmethod
    async def get_awstextract_data(file_bytes: bytes) -> Dict:
        global_blocks = []
        key_map = []
        value_map = []
        block_map = []
        global_value_map = []
        global_key_map = []
        global_blocks_for_getting_table_data = []

        # Create a stream from the byte array
        stream = BytesIO(file_bytes)

        # Initialize AWS Textract client
        textract_client = boto3.client('textract')

        # Analyze the document
        analyze_document_request = {
            'Document': {
                'Bytes': stream.getvalue()
            },
            'FeatureTypes': ['FORMS', 'TABLES']
        }
        analyze_document_response = textract_client.analyze_document(**analyze_document_request)

        # Get the text blocks
        blocks = analyze_document_response['Blocks']
        global_blocks = blocks

        # Get key-value maps
        for block in blocks:
            block_map.append(block)
            if block['BlockType'] == 'KEY_VALUE_SET':
                if 'KEY' in block['EntityTypes']:
                    key_map.append(block)
                else:
                    value_map.append(block)

        global_value_map = value_map
        global_key_map = key_map

        # Get Key-Value relationship
        key_value_relationship = await AWSTextractService.get_kv_relationship(key_map, value_map, block_map)

        # Output JSON
        j_obj = AWSTextractService.output_json(global_blocks)
        return j_obj

    @staticmethod
    async def get_kv_relationship(key_map: List[Dict], value_map: List[Dict], block_map: List[Dict]) -> Dict:
        kvs = {}
        for block in key_map:
            value_block = await AWSTextractService.find_value_block(block, value_map)
            key = await AWSTextractService.get_text(block, block_map)
            key = f"{key},|{block['Id']}"
            val = await AWSTextractService.get_text(value_block, block_map)
            val = f"{val},|{value_block['Id']}"
            if key not in kvs:
                kvs[key] = val
        return kvs

    @staticmethod
    async def find_value_block(block: Dict, value_map: List[Dict]) -> Dict:
        value_block = {}
        for relationship in block['Relationships']:
            if relationship['Type'] == 'VALUE':
                value_block_id = relationship['Ids'][0]
                value_block = next((value for value in value_map if value['Id'] == value_block_id), {})
        return value_block

    @staticmethod
    async def get_text(result: Dict, block_map: List[Dict]) -> str:
        text = ''
        for relationship in result['Relationships']:
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    word = next((block for block in block_map if block['Id'] == child_id), {})
                    if word['BlockType'] == 'WORD':
                        text += word['Text'] + ' '
                    elif word['BlockType'] == 'SELECTION_ELEMENT':
                        if word['SelectionStatus'] == 'SELECTED':
                            text += 'X '
        return text

    @staticmethod
    def output_json(blocks: List[Dict]) -> Dict:
        array = []
        for block in blocks:
            block_obj = {
                'BlockType': block['BlockType'],
                'Text': block.get('Text', ''),
                'Confidence': block.get('Confidence', ''),
                'TextType': block.get('TextType', ''),
                'RowIndex': block.get('RowIndex', ''),
                'ColumnIndex': block.get('ColumnIndex', ''),
                'RowSpan': block.get('RowSpan', ''),
                'ColumnSpan': block.get('ColumnSpan', ''),
                'Geometry': {
                    'BoundingBox': {
                        'Width': block['Geometry']['BoundingBox']['Width'],
                        'Height': block['Geometry']['BoundingBox']['Height'],
                        'Left': block['Geometry']['BoundingBox']['Left'],
                        'Top': block['Geometry']['BoundingBox']['Top']
                    },
                    'Polygon': [
                        {'X': point['X'], 'Y': point['Y']} for point in block['Geometry']['Polygon']
                    ]
                },
                'Id': block['Id'],
                'Page': block['Page']
            }
            if 'Relationships' in block:
                block_obj['Relationships'] = [
                    {'Type': relation['Type'], 'Ids': relation['Ids']} for relation in block['Relationships']
                ]
            if 'EntityTypes' in block:
                block_obj['EntityTypes'] = block['EntityTypes']
            array.append(block_obj)
        document = {
            'DocumentMetadata': {'Pages': 1},
            'JobStatus': 'SUCCEEDED',
            'Blocks': array,
            'AnalyzeDocumentModelVersion': '1.0'
        }
        return document

