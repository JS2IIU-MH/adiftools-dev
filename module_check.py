from setuptools import find_packages

# setup.pyでpackagesに設定した内容が想定通りになっているか？
if __name__ == '__main__':
    print(find_packages(include=['adiftools', 'adiftools.*'], exclude=['test/']))
