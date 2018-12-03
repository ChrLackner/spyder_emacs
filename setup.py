from setuptools import find_packages, setup

REQUIREMENTS = ['spyder']

setup(
    name='spyder-emacs',
    version='0.1',
    keywords='spyder emacs integration',
    license='MIT',
    author='Christopher Lackner',
    description='Emacs integration in Spyder',
    long_description="This Spyder plugin replaces the editor with emacs. It works only on X11",
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=REQUIREMENTS,
    include_package_data=True,
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 3']
)

