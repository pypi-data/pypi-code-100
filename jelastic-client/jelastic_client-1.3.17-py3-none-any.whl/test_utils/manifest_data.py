def get_manifest_data(success_text):
    if not success_text:
        return {}

    manifest_data = {}
    for key_value in success_text.split('<br />\n'):
        split_item = key_value.split(':')
        key = split_item[0]
        value = split_item[1]
        # to make it more flexible we could use re.sub
        # and try to extract code contained within optional
        # html tags
        key = key.replace('<strong>', '')
        key = key.replace('</strong>', '')
        manifest_data[key] = value.strip()

    return manifest_data
