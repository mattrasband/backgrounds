from pathlib import Path
from setuptools import setup

PROJECT_DIR = Path(__file__).parent


def read(path: Path) -> str:
    with open(path) as f:
        return f.read()


setup(author='Matt Rasband',
      author_email='matt.rasband@gmail.com',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.6',
      ],
      description='Desktop wallpaper/background downloader',
      entry_points={
          'console_scripts': [
              'backgrounds=backgrounds.__main__:main',
          ],
      },
      install_requires=[],
      license='MIT',
      long_description=read(PROJECT_DIR / 'README.md'),
      name='backgrounds',
      packages=[
          'backgrounds'
      ],
      url='https://github.com/mrasband/backgrounds',
      version='0.0.0a1')
