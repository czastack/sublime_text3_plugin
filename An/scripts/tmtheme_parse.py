from xml.etree import ElementTree

text = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>name</key>
    <string>Monokai Soda</string>
    <key>settings</key>
    <array>
        <dict>
            <key>settings</key>
            <dict>
                <key>background</key>
                <string>#222222</string>
                <key>caret</key>
                <string>#F8F8F0</string>
            </dict>
        </dict>
    </array>
</dict>
</plist>
'''


key_stack = []


def parse(node, parent=None):
    tag = node.tag
    data = None

    if tag == 'plist' or tag == 'array':
        data = []
        for child in node:
            parse(child, data)

    elif tag == 'dict':
        data = {}
        for child in node:
            parse(child, data)

    elif tag == 'string':
        data = node.text or ''

    elif tag == 'key':
        key_stack.append(node.text)

    if parent is not None and data is not None:
        if isinstance(parent, list):
            parent.append(data)
        elif isinstance(parent, dict):
            parent[key_stack.pop()] = data

    return data


root = ElementTree.fromstring(text)
data = parse(root)

print(data)
