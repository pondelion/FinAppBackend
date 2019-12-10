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

        responses = []
        try:
            table = DYNAMO_DB.Table(table_name)
        except Exception as e:
            Logger.e('DynamoDB#put_item', f'Failed at DYNAMO_DB.Table(table_name) : {e}')
            raise e

        if use_batch_writer:
            with table.batch_writer() as batch:
                for item in items:
                    try:
                        responses.append(
                            batch.put_item(
                                Item=item,
                            )
                        )
                    except Exception as e:
                        Logger.e('DynamoDB#put_item', f'Failed to put data to DynamoDB. Skipping : {e}')
        else:
            for item in items:
                try:
                    responses.append(
                        table.put_item(
                            TableName=table_name,
                            Item=item,
                        )
                    )
                except Exception as e:
                    Logger.e('DynamoDB#put_item', f'Failed to put data to DynamoDB. Skipping : {e}')

        return responses
