import os
from time import sleep

class Config():

    def __init__(self, path:str, mode:str=None, owner:str=None, description=None):
        self.path = path
        # check path
        if self.path != None:
            self.file_check_create(self.path, mode, owner, description)
        #
        self._dict = {}
        self.read()

    def __getitem__(self, key):
        return self._dict[key]
    
    def __setitem__(self, key, value):
        self._dict[key] = value


    def file_check_create(self, path:str, mode:str=None, owner:str=None, description=None):
        dir = path.rsplit('/', 1)[0] # rsplit(), split from right; split(), split from left
        try:
            # check file
            if os.path.exists(path):
                if not os.path.isfile(path):
                    print('Could not create file, there is a folder with the same name')
                    return
                else:
                    # file already exists
                    pass
            else:
                # check directory
                if os.path.exists(dir):
                    if not os.path.isdir(dir):
                        print('Could not create file, there is a file with the same name')
                        return
                    else:
                        # dir already exists
                        pass
                else:
                    # create directory
                    os.makedirs(dir, mode=0o754) # makedirs， make multi-level directories
                    sleep(0.001)

                # create file
                with open(path, 'w') as f:
                    if description != None:
                        lines = description.split('\n')
                        _desc = ''
                        for line in lines:
                            _desc += '# '+line+'\n'
                        _desc += '\n'
                        f.write(_desc)
                    else:
                        f.write('')

                # set mode
                if mode != None:
                    os.popen('sudo chmod %s %s'%(mode, path))
                # set owner
                if owner != None:
                    os.popen('sudo chown -R %s:%s %s'%(owner, owner, dir))
        except Exception as e:
            raise(e)

    @staticmethod
    def _read(path):
        _dict = {}
        with open(path, 'r') as f:
            lines = f.readlines()
            section = ''
            _dict[section] = {}
            for line in lines:
                line = line.strip()
                if len(line) == 0:
                    continue
                if line[0] == '#':
                    continue
                elif line[0] == '[':
                    section = line[1:-1].strip()
                    _dict[section] = {}
                elif '=' in line:
                    option, value = line.split('=', 1)
                    option = option.strip()
                    value = value.strip()
                    # print(section, option, value)
                    _dict[section][option] = value
                else:
                    pass
        return _dict

    @staticmethod
    def _write(path, dict):
        part = {}
        _dict = dict.copy()
        # print(id(_dict), id(dict))
        _sections = list(_dict.keys())
        # print(f'_sections: {_sections}')
        with open(path, 'r') as f:
            lines = f.readlines()
            section = ''
            part[section] = []
            for line in lines:
                line = line.strip()
                if len(line) == 0:
                    part[section].append('\n')
                elif line[0] == '#':
                    part[section].append(line+'\n')
                elif line[0] == '[':
                    # fill items not added in last section
                    if section in _sections:
                        for option, value in _dict[section].items():
                            part[section].append(f'{option} = {value}\n')
                        _dict.pop(section)
                    # next section
                    section = line[1:-1].strip()
                    part[section] = []
                    part[section].append(line+'\n')
                elif '=' in line:
                    option, value = line.split('=', 1)
                    option = option.strip()
                    value = value.strip()
                    if section in _sections and option in _dict[section].keys():
                        value = _dict[section][option]
                        _dict[section].pop(option)
                    part[section].append(f'{option} = {value}\n')
                else:
                    part[section].append(line+'\n')
            # --------------------------------------------------
            # fill items not added in last section
            if section in _sections:
                for option, value in _dict[section].items():
                    part[section].append(f'{option} = {value}\n')
                _dict.pop(section)

            # print(f'new sections: {_dict.keys()}')
            sections = list(_dict.keys())
            for _section in sections:
                part[_section] = []
                part[_section].append(f'[{_section}]\n')
                for option, value in _dict[_section].items():
                    part[_section].append(f'{option} = {value}\n')
                part[_section].append('\n')
                _dict.pop(_section)

        # write new contents to file
        with open(path, 'w') as f:
            for _section in part.keys():
                for line in part[_section]:
                    f.write(line)

        # print new contents
        # for _section in part:
        #     for line in part[_section]:
        #         print(line, end='', flush=True)

    def read(self):
        self._dict = self._read(self.path)
        return self._dict

    def write(self):
        self._write(self.path, self._dict)

    def get(self, section, option, default=None):
        if section not in self._dict.keys():
            self._dict[section] = {}
            self._dict[section][option] = str(default)
        elif option not in self._dict[section].keys():
            self._dict[section][option] = str(default)
        #
        return self._dict[section][option]

    def set(self, section, option, value):
        if section not in self._dict.keys():
            self._dict[section] = {}
        self._dict[section][option] = value


if __name__ == '__main__':
    # description = 'robot-hat config test\nhello'
    description = '''
    robot-hat config test
    hello
    world
'''
    config = Config(path='/opt/robot-hat/test.config',
                    mode='775',
                    owner='xo', 
                    description=description)

    print(config.read()) # read config file to dict

    config['section1'] = {}
    config['section1']['option1'] = '1234'

    config['section2'] = {'option1': '100'}
    print(config.read())
 
    config.write() # write dict to config file

    print(config.get('section2', 'option1'))
    print(config.get('section3', 'option1', default='hello'))

    config.set('section4', 'option1', 'hi')
    config.write()



