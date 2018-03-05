import os
from shutil import copy2
import filetype


class Ali(object):
    """docstring for Ali"""

    def __init__(self):
        super(Ali, self).__init__()
        self.gather = 'SET'
        self.pwd = os.getcwd()

    def files_extracter(self):
        # 获取当前目录下所有目录列表
        dir_list = []
        file_path_list = []
        print('trying to copy files from floders to SET...')
        all_list = os.listdir(self.pwd)
        for dir in all_list:
            if os.path.isdir(dir) is True:
                dir_list.append(dir)
        # print(dir_list)
        os.makedirs(self.gather, exist_ok=True)
        # 遍历所有目录
        for d in dir_list:
            files_list = os.listdir(d)
            # 遍历各目录下文件，获得文件名列表。
            for file in files_list:
                file_path = os.path.join(os.path.join(self.pwd, d), file)
                # 判断是否为文件
                if os.path.isfile(os.path.join(os.path.join(self.pwd, d), file)) is True:
                    try:
                        copy2(file_path, os.path.join(self.pwd, self.gather))
                    except IOError as e:
                        print(e)
                    # print(file_path)
                    # file_path_list.append(file_path)

        # print(len(set(file_path_list)))

    def renamer(self):
        print('trying to rename files which without extension name')
        files = os.listdir(os.path.join(self.pwd, self.gather))
        for i in files:
                    # print(files.pop())
            one = os.path.join(os.path.join(self.pwd, self.gather), i)
            extension = self.guesser(one)
            # print(one)
            if extension is not None:
                try:
                    os.rename(one, one + '.' + extension)
                except IOError as e:
                    print(e)
            else:
                continue
                # print('Unknown Type, rename failed.')
        print('Total File: ' + str(len(files)))
        print('Now complete')

    def guesser(self, file):
        kind = filetype.guess(file)
        if kind is None:
            print('Cannot guess file type!')
            return

        # print('File extension: %s' % kind.extension)
        # print('File MIME type: %s' % kind.mime)
        return kind.extension

    def main(self):
        self.files_extracter()
        self.renamer()


if __name__ == '__main__':
    print('initializing... plz wait a moment')
    ali = Ali()
    ali.main()
    input()
