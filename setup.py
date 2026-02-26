from setuptools import setup, find_packages

setup(
    name="not_napping",
    version="2.0.0",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "pyautogui>=0.9.53",
        "setproctitle>=1.3",
    ],
    entry_points={
        "console_scripts": [
            "not-napping=not_napping.cli:main",
        ],
    },
)
