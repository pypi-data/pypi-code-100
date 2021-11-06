def get_type_from_id(stix_id: str) -> str:
    return stix_id.split('--', maxsplit=1)[-1]


def is_id(stix_id: str) -> bool:
    return '--' in stix_id
