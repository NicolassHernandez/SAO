from setuptools import setup, find_packages

setup(
    name='sao',                 # Name of your package
    version='1.3.0',                   # Version number
    author='Nicolas et al',                # Your name
    author_email='nicolas.hernandez@pucv.cl',  # Your email
    description='A brief description of your package',
    long_description=open('READMErst').read(),  # Optional: Long description from README
    long_description_content_type='text/markdown',  # Optional: Content type for long description
    url='https://github.com/NicolassHernandez/SAO',  # URL of your package repository
    packages=find_packages(),          # Automatically find and include all packages
    classifiers=[                      # Optional: Classifiers help users find your package
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',           # Python version requirement
    install_requires=[                 # Optional: List of dependencies
        'somepackage>=1.0',
        'anotherpackage>=2.0',
    ],
    include_package_data=True,         # Include additional files specified in MANIFEST.in
)
