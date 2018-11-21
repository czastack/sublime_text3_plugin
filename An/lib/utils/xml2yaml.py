import xml.etree.ElementTree as ET


class Xml2yaml(object):
    """
    it = Xml2yaml()
    it.parse(file)
    print(it.toyaml())
    """
    events = ("end", "start")

    def parse(self, file):
        self.stack = []
        self.put = None
        for event, elem in ET.iterparse(file, events=self.events):
            start = event == "start"
            if elem.tag == 'array':
                if start:
                    cur = []
                    self.put and self.put(cur)
                    self.__push(cur)
                else:
                    self.__pop()
            elif elem.tag == 'dict':
                if start:
                    cur = {}
                    self.put and self.put(cur)
                    self.__push(cur)
                else:
                    self.__pop()
            elif elem.tag == 'key':
                if not start:
                    self.key = elem.text
            elif elem.tag == 'string' and not start:
                if self.key != 'uuid':
                    self.put(elem.text)

    def __push(self, target):
        self.stack.append(target)
        self.__update_put()

    def __pop(self):
        tmp = self.stack.pop()
        if self.stack:
            self.__update_put()
        else:
            self.root = tmp

    def __update_put(self):
        cur = self.stack[-1]
        if isinstance(cur, list):
            self.put = cur.append
        elif isinstance(cur, dict):
            self.put = self.__dict_put

    def __dict_put(self, value):
        self.stack[-1][self.key] = value

    def toyaml(self, long=False):
        import yaml
        data = {}
        if long:
            data['default_flow_style'] = False
        return yaml.dump(self.root, **data)
