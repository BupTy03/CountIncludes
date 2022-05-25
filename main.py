import sys
import os


class IncludesCollection:
    def __init__(self) -> None:
        self.includes = {}

    def add_from_line(self, line:str):
        pos = line.find('#include')
        if pos < 0:
            return

        pos += 8
        while pos < len(line) and (line[pos].isspace() or line[pos] == '"' or line[pos] == "<"):
            pos += 1
        
        start_pos = pos
        while pos < len(line) and not (line[pos].isspace() or line[pos] == '"' or line[pos] == ">"):
            pos += 1

        end_pos = pos
        if start_pos < end_pos:
            incl = line[start_pos:end_pos]
            if incl in self.includes:
                self.includes[incl] += 1
            else:
                self.includes[incl] = 1

    def add_from_file(self, filepath:str):
        if filepath.startswith('C:\Work\i3pro\libs'):
            return

        with open(filepath, 'r', encoding='utf-8') as source_file:
            while True:
                try:
                    line = source_file.readline()
                except:
                    print(f'Problem with file: {filepath}!')
                    continue

                if not line:
                    break
                
                self.add_from_line(line)

    def add_from_dict(self, dictpath:str):
        for root, dirs, files in os.walk(dictpath, topdown=True, onerror=None, followlinks=False):
            for filename in files:
                if filename.endswith(('.hpp', '.cpp', '.h', '.c')):
                    self.add_from_file(os.path.join(root, filename))

    def print(self):
        for include, count in sorted(self.includes.items(), key=lambda item: item[1]):
            print(f'{include}: {count}')

def simple_test():
    test_lines = [
        '#include <iostream>',
        '#include "my_header.h"'
    ]

    collection = IncludesCollection()
    for line in test_lines:
        collection.add_from_line(line)

    collection.print()

def main(args):
    collection = IncludesCollection()
    collection.add_from_dict(args[1])
    collection.print()

if __name__ == '__main__':
    main(sys.argv)
