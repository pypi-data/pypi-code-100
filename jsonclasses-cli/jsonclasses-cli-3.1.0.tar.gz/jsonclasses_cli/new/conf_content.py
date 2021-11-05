from typing import Literal


def conf_content(http_library: Literal['flask', 'fastapi'],
                include_user: bool,
                include_admin: bool) -> str:
    return """
{
    "operator": {
        "secretKey": "environ['OPERATOR_SECRET_KEY']"
    }
}
    """.strip() + '\n'
