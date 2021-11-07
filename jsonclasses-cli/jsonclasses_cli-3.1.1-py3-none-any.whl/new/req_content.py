from typing import Literal


def req_content(http_library: Literal['flask', 'fastapi'],
                include_user: bool,
                include_admin: bool) -> str:
    nl = '\n'
    return f"""
jsonclasses>=3.0.0,<4.0.0
jsonclasses-pymongo>=3.0.0,<4.0.0
jsonclasses-server>=3.0.0,<4.0.0
inflection>=0.5.1,<0.6.0
{'flask[async]>=2.0.1,<2.1.0' if http_library == 'flask' else 'fastapi>=0.70.0,<0.71.0'}
python-dotenv>=0.19.1,<0.20.0{f'{nl}bcrypt>=3.2.0,<4.0.0' if include_admin or include_user else ''}
    """.strip() + '\n'
