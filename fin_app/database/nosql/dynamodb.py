from typing import List, Dict

from ...aws.resource_provider import DYNAMO_DB
from ...utils.logger import Logger


class DynamoDB:

    @staticmethod
    def put_items(
        table_name: str,
        items: List[Dict],
        use_batch_writer: bool = False,
    ) -> List:
        """[summary]
        
        Args:
            table_name (str): [description]
            items (List[Dict]): [description]
        
        Raises:
            e: [description]
        
        Returns:
            List: [description]
        """
        if not isinstance(items, list):
            items = [items]

        if use_batch_writer:
            try:
                table = DYNAMO_DB.Table(table_name)
                with table.batch_writer() as batch:
                    responses = [
                        batch.put_item(
                            Item=item,
                        ) for item in items
                    ]
            except Exception as e:
                Logger.e('DynamoDB#put_item', f'Failed to put data to DynamoDB : {e}')
                raise e
        else:
            try:
                table = DYNAMO_DB.Table(table_name)
                responses = [
                    table.put_item(
                        TableName=table_name,
                        Item=item,
                    ) for item in items
                ]
            except Exception as e:
                Logger.e('DynamoDB#put_item', f'Failed to put data to DynamoDB : {e}')
                raise e

        return responses
