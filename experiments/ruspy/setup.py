from setuptools import setup

setup(
    name="ruspy",
    version="1.0",
    py_modules=["ruspy"],
    entry_points={
        "console_scripts": [
            "ruspy = ruspy:main",
        ],
    },
)
