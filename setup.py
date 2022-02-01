from setuptools import setup, find_packages

setup(
    name='python_samples',
    packages=find_packages(where='samples'),
     package_dir={
        '': 'samples',
    },
    version='1.0.0',
    author='Anton Sylantiev',
    install_requires=[
      'requests==2.26.0',
      'python-dotenv==0.19.1',
      'pytest==6.2.5'
    ]
)