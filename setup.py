import codecs
import os

import setuptools


here = os.path.abspath(os.path.dirname(__file__))

with codecs.open("README.md", "r", "utf-8") as f:
    readme = f.read()

about = {}
with codecs.open(
    os.path.join(here, "mbq", "ranch", "__version__.py"), "r", "utf-8"
) as f:
    exec(f.read(), about)

setuptools.setup(
    name=about["__title__"],
    description=about["__description__"],
    long_description=readme,
    long_description_content_type="text/markdown",
    version=about["__version__"],
    license=about["__license__"],
    url=about["__url__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    maintainer=about["__author__"],
    maintainer_email=about["__author_email__"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries",
    ],
    keywords="",
    package_data={"mbq.ranch": ["py.typed"]},
    packages=setuptools.find_packages(),
    install_requires=[
        "arrow",
        "celery<5.0",
        "mbq.env>=2,<3",
        "mbq.metrics>=1,<2",
        "rollbar",
    ],
    zip_safe=False,
)
