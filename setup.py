from setuptools import setup
import re

with open('chparse\\__init__.py') as f:
    content = f.read()
    longdesc = re.match(r'^"""([\s\S]+?)"""', content).group(1).strip()
    with open('README.rst', 'w') as rdme:
        rdme.write(longdesc)
    version = re.search(r'__version__\s*=\s*"([^"]+)"', content).group(1)
del f, rdme

setup(
    name="mw-api-client",
    version=version,
    description="Parse Clone Hero charts with ease!.",
    long_description=longdesc,
    url="https://github.com/Kenny2github/chparse",
    author="Ken Hilton",
    license="GPLv3+",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Markup',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6'
    ],
    keywords='file format parser',
    packages=['chparse'],
    python_requires='>=2.7',
    test_suite='nose.collector',
    tests_require=['nose'],
)
