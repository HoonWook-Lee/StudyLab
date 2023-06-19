from boto3 import client, resource
from config.settings import env


# AWS SDK : 비교적 로울 레벨 접근이 가능
my_client = client(
    'dynamodb',  
    aws_access_key_id = env('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key = env('AWS_SECRET_ACCESS_KEY'),
    region_name = 'ap-northeast-2'
)
# client를 래핑한 고수준의 서비스
my_resource = resource(
    'dynamodb',  
    aws_access_key_id = env('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key = env('AWS_SECRET_ACCESS_KEY'),
    region_name='ap-northeast-2'
)

# 댓글 테이블 
Comments = my_resource.Table('Comments')

# 댓글 테이블 존재 유무 확인 후 없다면 생성
def table_existence():
    try:
        my_client.describe_table(TableName='Comments')
    except:
        my_resource.create_table(
            TableName='Comments',                  # 테이블 명
            KeySchema = [                          # 키 스키마
                {
                    'AttributeName': 'Memo',
                    'KeyType': 'HASH'              # Partition key
                },
                {
                    'AttributeName': 'Created_at',
                    'KeyType': 'RANGE'             # Sort Key
                }
            ],
            AttributeDefinitions = [               # 선언된 키와 인덱스 속성
                {
                    'AttributeName': 'Memo',
                    'AttributeType': 'N'           # Partition key
                },
                {
                    'AttributeName': 'Created_at',
                    'AttributeType': 'S'           # Sort Key
                }
            ],
            # 읽기, 쓰기에 사용할 유닛(=동시에 처리 가능한 트랜잭션의 수)의 수를 정하는 옵션
            ProvisionedThroughput = {              
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )