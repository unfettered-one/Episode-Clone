from setuptools import setup, find_packages

setup(
    name="episode_backend",
    version="0.1.0",
    packages=find_packages(),
    # pip install -e ./app --config-settings editable_mode=compat
    install_requires=[
        "fastapi==0.116.1",
        "uvicorn==0.35.0",
        "faiss-cpu==1.11.0",
        "openai==1.97.1",
        "langchain==0.3.27",
        "tiktoken==0.9.0",
        "langchain-community==0.3.27",
        "sentence-transformers"
    ],
    entry_points={
        "console_scripts": [],
    },
)
