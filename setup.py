import setuptools

setuptools.setup(
    name="scspkg",
    packages=setuptools.find_packages(),
    scripts=['bin/scspkg'],
    version="0.0.1",
    author="Luke Logan",
    author_email="llogan@hawk.iit.edu",
    description="Helps build modulefiles",
    url="https://github.com/scs-lab/scspkg",
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 0 - Pre-Alpha",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: None",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Application Configuration",
    ],
    long_description="",
    install_requires=[
        'jarvis-util @ git+https://github.com/scs-lab/jarvis-util.git#egg=jarvis-util'
    ]
)
