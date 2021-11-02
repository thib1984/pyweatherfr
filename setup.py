from setuptools import setup


setup(
    name="pyweather",
    version="0.0.1",
    description="pyweather displays weather forecast for a given town in France",
    long_description="The complete description/installation/use/FAQ is available at : https://github.com/thib1984/pyweather#readme",
    url="https://github.com/thib1984/pyweather",
    author="thib1984",
    author_email="thibault.garcon@gmail.com",
    license="MIT",
    packages=["pyweather"],
    install_requires=[],
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "pyweather=pyweather.__init__:pyweather"
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
