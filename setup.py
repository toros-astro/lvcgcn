from setuptools import setup

# Get the version from astroalign file itself (not imported)
with open('torosgcn/__init__.py', 'r') as f:
    for line in f:
        if line.startswith('__version__'):
            _, _, lst_version = line.replace("'", '').split()
            break

setup(name='torosgcn',
      version=lst_version,
      description='LVC-GCN Alert Processor',
      author='TOROS Dev Team',
      author_email='martinberoiz@gmail.com',
      url='https://github.com/toros-astro/alert-robot',
      packages=['torosgcn',],
      install_requires=["pygcn",
                        "numpy",
                        "scipy",
                        "astropy",
                        "healpy",
                        "requests",
                        "pyyaml",
                        "loguru",
                        ],
      test_suite='tests',
      entry_points={
        'console_scripts': [
            'lvcgcn = torosgcn.listen:main',
        ],
      },
      )
