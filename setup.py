#!/usr/bin/env python3

from setuptools import setup

setup(name="SuperCoder",
      version="2.0",
      description="""Meet and help in the development, improvements and 
      corrections of Open Source software""",
      author="Valter Nazianzeno (manipuladordedados)",
      author_email="manipuladordedados@gmail.com",
      url="https://github.com/manipuladordedados/SuperCoder",
      license="GNU GPLv3",
      requires=["beautifulsoup4", "PyQt5 (>=5.1)"],      
      packages=["SuperCoder"],
      package_data={"SuperCoder": ["img/*", "LICENSE"]},
      data_files=[("share/applications", ["SuperCoder.desktop"]),
                  ("share/pixmaps", ["SuperCoder/img/SuperCoder.png"])],
      scripts=["bin/SuperCoder", "bin/SuperCoder-cli"],
      classifiers=['License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.2',
                   'Programming Language :: Python :: 3.3',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5',
                   'Development Status :: 5 - Production/Stable',
                   'Intended Audience :: Developers',         
                   'Topic :: Software Development'])
