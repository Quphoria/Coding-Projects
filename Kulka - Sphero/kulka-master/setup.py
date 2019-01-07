from setuptools import setup


def requirements():
    import socket

    if hasattr(socket, 'AF_BLUETOOTH'):
        return []

    return ['pybluez']


setup(
    name='Kulka',
    version='0.3.0',
    description='Sphero client',
    author='Karol Szuster',
    author_email='szuster.karol@gmail.com',
    url='https://github.com/karulis/pybluez',
    install_requires=requirements(),
    packages=[
        'kulka',
        'kulka.connection',
        'kulka.connection.exceptions',
        'kulka.core',
        'kulka.request',
        'kulka.response',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Communications'
    ],
    download_url='https://github.com/karulis/pybluez',
    maintainer='Karol Szuster',
    license='GPL'
)
