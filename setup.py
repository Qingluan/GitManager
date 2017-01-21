

from setuptools import setup, find_packages


setup(name='gire',
    version='1.2',
    description='a tool to manage remote git server\'s projects ',
    url='https://github.com/Qingluan/.git',
    author='Qing luan',
    author_email='darkhackdevil@gmail.com',
    license='MIT',
    zip_safe=False,
    packages=find_packages(),
    install_requires=['hackcmds==5.1','mroylib-min==1.0'],
    entry_points={
        'console_scripts': ['gIre=gire.create:main']
    },

)


