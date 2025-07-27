from setuptools import setup, find_packages

setup(
    name="episode_backend",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn[standard]"
    ],
    entry_points={
        "console_scripts": [],
    },
)
