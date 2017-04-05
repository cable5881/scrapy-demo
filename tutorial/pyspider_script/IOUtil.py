import os

DIR_PATH = 'g:/img'

class IOUtil(object):
    def __init__(self):
        self.path = DIR_PATH
        if not self.path.endswith('/'):
            self.path = self.path + '/'
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def mkDir(self, path):
        path = path.strip()
        dir_path = self.path + path

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    def save(self, content, path):
        absolute_path = self.path + path
        f = open(absolute_path, 'wb')
        f.write(content)
        f.close()

    def getExtension(self, url):
        extension = url.split('.')[-1]
        return extension  