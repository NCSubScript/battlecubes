from setuptools import setup, find_packages

setup(
    name="game_project",
    version="0.1.0",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        "pygame",
        "steamworks",
    ],
    entry_points={
        "console_scripts": [
            "game_project=main:main",
        ],
    },
)
