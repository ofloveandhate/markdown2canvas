from setuptools import find_packages, setup

EXCLUDE_FROM_PACKAGES = []


extras = {}

setup(name='markdown2canvas',
      version='0.0',  # TODO make this set programmatically
      description='code for publishing markdown documents to Canvas pages',
      url='https://github.com/ofloveandhate/markdown2canvas',
      author='Silviana Amethyst',
      author_email='amethyst@uwec.edu',
      packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
      install_requires=['canvasapi','emoji','markdown', 'beautifulsoup4','Pygments'],
      extras_require=extras,
      package_dir={'markdown2canvas': 'markdown2canvas'},
      zip_safe=False)
