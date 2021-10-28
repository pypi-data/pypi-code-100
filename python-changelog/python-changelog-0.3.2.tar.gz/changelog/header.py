def remove_header(old_changelog):
    header = []
    while not old_changelog[0] or old_changelog[0].startswith('# '):
        header.append(old_changelog[0])
        old_changelog.pop(0)
    return '\n'.join(header) + '\n'

def generate_header(name):
    return f"# { name } Changelog\n\n"
