#!/usr/bin/env python3
import sys
import argparse
import datetime
from xml.etree import ElementTree

def getprerelease(tag):
    # We expect the tag to have the form vMAJOR.MINOR.REVISION-rcCANDIDATE
    # Strip off the leading v from the tag and turn the rcCANDIDATE bit into
    # a pre-release suffix.
    version = tag.replace('-', '~', 1)
    if version[0] == 'v':
        version = version[1:]

    attrs = {
        'version': version,
        'type': 'development',
        'date': datetime.date.today().isoformat()
    }
    entry = ElementTree.Element('release', attrib=attrs)

    xurl = ElementTree.Element('url', attrib={'type': 'details'})
    xurl.text = f'https://github.com/mozilla-mobile/mozilla-vpn-client/releases/tag/{tag}'
    entry.append(xurl)

    return entry

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Insert a pre-release into an Appstream release file")
    parser.add_argument('manifest', metavar='FILE', type=str, action='store',
        help='Appstream release manifest')
    parser.add_argument('-t', '--tag', metavar='NAME', type=str, required=True,
        help='Git release tag')
    parser.add_argument('-i', '--inplace', action='store_true',
        help='Modify release manifest in-place')
    args = parser.parse_args()

    # Load the release manifest
    tree = ElementTree.parse(args.manifest)
    root = tree.getroot()

    # Insert the pre-release tag and output the result
    root.insert(0, getprerelease(args.tag))
    ElementTree.indent(root, space="  ")
    if args.inplace:
        tree.write(args.manifest)
    else:
        ElementTree.dump(root)
