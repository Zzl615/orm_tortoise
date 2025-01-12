from pydantic import BaseModel
from typing import Union


class FieldCondition(BaseModel):
    type: str
    field: str


class OptionItem(BaseModel):
    left: FieldCondition
    op: str
    right: str


class Condition(BaseModel):
    id: str
    conjunction: str
    children: List[Union['Condition', OptionItem]]


def generate_sql_query(condition: Condition) -> str:
    if condition.conjunction == 'or':
        conjunction = 'or'
    else:
        conjunction = 'and'
    if condition.children:
        children = [generate_sql_query(child) for child in condition.children]
        return f'({conjunction.join(children)})'
    else:
        return f'{condition.left.field} {condition.op} {condition.right}'


# 测试数据
data = {
    "conditions": {
        "id": "837888e1932a",
        "conjunction": "or",
        "children": [
            {
                "id": "ead2c8b8ea50",
                "left": {
                    "type": "field",
                    "field": "text"
                },
                "op": "equal",
                "right": "123"
            },
            {
                "id": "65d57326757e",
                "conjunction": "or",
                "children": [
                    {
                        "id": "041f02987794",
                        "left": {
                            "type": "field",
                            "field": "text"
                        },
                        "op": "equal",
                        "right": "23"
                    },
                    {
                        "id": "ec4e7f4b8b71",
                        "left": {
                            "type": "field",
                            "field": "text"
                        },
                        "op": "not_equal",
                        "right": "2345"
                    }
                ]
            }
        ]
    }
}

# 校验规则并生成 SQL 查询语句
parsed_condition = Condition.parse_obj(data['conditions'])
import pdb; pdb.set_trace()
sql_query = generate_sql_query(parsed_condition)
print(sql_query)


{
  "title": "查询条件",
  "columnCount": 3,
  "mode": "horizontal",
  "body": [
    {
      "type": "input-text",
      "label": "  方案名",
      "name": "name",
      "id": "u:48b44f0fa587"
    },
    {
      "type": "input-text",
      "label": "目标用户",
      "name": "user_targets",
      "id": "u:ffada59dfc54"
    },
    {
      "type": "input-text",
      "label": "创建者",
      "name": "creator_ids",
      "id": "u:5eaf3d92c97a"
    },
    {
      "type": "input-text",
      "label": "创建时间",
      "name": "create_time",
      "id": "u:a049b1e15134"
    }
  ],
  "id": "u:76f5abe10fdc"
}