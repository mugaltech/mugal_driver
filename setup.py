"""Device drivers for MugalTech products.
See:
https://github.com/mugaltech/mugal_driver
"""

from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='mugal_driver',
    version='0.1.0', 
    description='Device drivers for MugalTech products', 
    long_description=long_description,
    long_description_content_type='text/markdown',
   url='https://github.com/mugaltech/mugal_driver', 
    author='BenFre',
   author_email='bingcheng7757@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: System :: Hardware :: Hardware Drivers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "Programming Language :: Python :: 3.10",
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='driver, signal generator',
    package_dir={'': 'src'},  
    packages=find_packages(where='src'), 
    python_requires='>=3.6, <4',
    install_requires=['pyserial', 'libscrc'], 
    #package_data={  
    #    'sample': ['package_data.dat'],
    #},
    #entry_points={
    #    'console_scripts': [
    #        'sample=sample:main',
    #    ],
    #},
    project_urls={ 
        'Bug Reports': 'https://github.com/mugaltech/mugal_driver/issues',
        'Source': 'https://github.com/mugaltech/mugal_driver',
    },
)
