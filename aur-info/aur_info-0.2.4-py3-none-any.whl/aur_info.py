#!/bin/python

def __get_node_value(html_node, node_name):
    tag = html_node.findChildren('th', text='{}: '.format(node_name))[0]
    vtag = tag.next.next.next
    if 'Git' in node_name:
        return vtag.a.text
    return vtag.text

def get_info(pkg_name):
    import requests as r
    from bs4 import BeautifulSoup as bs

    pkg = {}
    res = r.get('https://aur.archlinux.org/packages/{}'.format(pkg_name))
    if not res.ok:
        return None
    pkg['name']=pkg_name.capitalize()
    b = bs(res.text, 'html.parser')
    table_info = b.body.select('table[id=pkginfo]')[0]
    pkg['maintainer'] = __get_node_value(table_info, 'Maintainer')
    pkg['last_packager'] = __get_node_value(table_info, 'Last Packager')
    pkg['votes'] = int(__get_node_value(table_info, 'Votes'))
    pkg['popularity'] = float(__get_node_value(table_info, 'Popularity'))
    pkg['created'] = __get_node_value(table_info, 'First Submitted')
    pkg['description'] = __get_node_value(table_info, 'Description')
    pkg['git_url'] = __get_node_value(table_info, 'Git Clone URL')
    pkg['updated'] = __get_node_value(table_info, 'Last Updated')
    pkg['version']=b.body.select('div[id=pkgdetails]')[0].h2.text.split()[3]
    pkg['submitted']=b.body.table.findChildren("tr")[-2].td.text
    pkg['updated']=b.body.table.findChildren("tr")[-1].td.text
    return pkg

if __name__ == '__main__':
    import os
    import sys

    av = sys.argv[1:]
    if len(av) == 0 or av[0]=='':
        print('Usage: aur-info <package_name>')
        exit(1)

    pkg = get_info(av[0])
    if pkg:
        print("""
\nName: {}
Description: {}
Maintainer: {}
Last Packager: {}
Votes: {}
Popularity: {}
Version: {}
Created: {}
Updated: {}
Git: {}

        """.format(
            pkg['name'],
            pkg['description'],
            pkg['maintainer'],
            pkg['last_packager'],
            pkg['votes'],
            pkg['popularity'],
            pkg['version'],
            pkg['created'],
            pkg['updated'],
            pkg['git_url']
        ))
    else:
        raise Exception("Package not found. Please check to see if there exists a match.")
