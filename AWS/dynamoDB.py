import boto3
from decimal import Decimal
from boto3.dynamodb.conditions import Attr

class DynamoDBHelper:
    def __init__(self, table_name):
        self.table_name = table_name
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(self.table_name)

    def get_item_by_name(self, name):
        try:
            response = self.table.scan(FilterExpression=Attr('name').eq(name))
            items = response.get('Items', [])
            if items:
                return items[0]  # Assuming name is unique, so we return the first match
        except Exception as e:
            print(f"An error occurred while querying the table: {e}")
        return None
    
    def get_complete_table(self):
        try:
            response = self.table.scan()
            items = response.get('Items', [])
            return items
        except Exception as e:
            print(f"An error occurred while looking up table: {e}")
        return None

    def print_items(self, items):
        for item in items:
            print(item)

def main():
    table_name = 'Student-academic-records'
    dynamodb_helper = DynamoDBHelper(table_name)
    name_to_query = 'morgan_freeman'

    # get complete table
    items = dynamodb_helper.get_complete_table()
    
    if items:
        dynamodb_helper.print_items(items)
    else:
        print(f"No item found with the name '{name_to_query}' in the table.")

if __name__ == "__main__":
    main()
