from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='outlines-unleashed',
    version='0.0.11',
    packages=['outline', 'tests', 'tests.outline', 'tests.outline_unleashed', 'resources', 'resources.test',
              'outlines_unleashed', 'outline_preprocessors', 'output_generators'],
    url='https://github.com/sevire/outlines-unleashed',
    license='TBD',
    author='Thomas Gaylard',
    author_email='thomas.gaylard@genonline.co.uk',
    description='Unleash the power of OPML and Outlines',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6', install_requires=['ddt']
)
