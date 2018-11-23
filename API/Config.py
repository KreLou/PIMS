
class Config():

    Values = dict();

    def __init__(self):
        print('Init');
        with open('../config', 'r') as file:
            for line in file:
                line_args = line.replace('\n', '').split('=')
                if len(line_args) != 2:
                    print('[Config] Could not read Config line: ', line)
                    continue
                key = line_args[0].lower()
                value = line_args[1]
                self.Values[key] = value
                print(key, ' -> ', value);


    def getValue(self, key):
        key = key.lower()
        if key in self.Values:
            return self.Values[key]
        else:
            return None