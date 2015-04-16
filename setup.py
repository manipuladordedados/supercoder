#!/usr/bin/env python

from setuptools import setup

setup(name="SuperCoder",
      version="1.0",
      description="""Meet and help in the development, improvements and 
      corrections of Open Source software""",
      author="Valter Nazianzeno (manipuladordedados)",
      author_email="manipuladordedados@gmail.com",
      url="https://github.com/manipuladordedados/SuperCoder",
      license="GNU GPLv2",
      packages=["SuperCoder"],
      package_data={'SuperCoder': ["img/*", "LICENSE"]},
      data_files=[("share/applications", ["SuperCoder.desktop"]),
                  ('share/pixmaps', ['SuperCoder/img/SuperCoder.png'])],
      scripts=["bin/SuperCoder", "bin/SuperCoder-cli"])