from setuptools import setup

setup(
    name='requests-sshadapter',
    version='0.1.0',
    description='A Requests adapter for connecting to HTTP servers through an '
                'SSH tunnel',
    long_description=(open('README.rst').read() + '\n\n' +
                      open('HISTORY.rst').read() + '\n\n' +
                      open('AUTHORS.rst').read()),
    url='http://github.com/samh/requests-sshadapter/',
    license='MIT',
    author='Sam Hartsfield',
    author_email='samh.public@gmail.com',
    py_modules=['requests_sshadapter'],
    include_package_data=True,
    install_requires=['requests', 'bgtunnel'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
