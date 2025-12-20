from setuptools import setup, find_packages

setup(
    name="episode_backend",
    version="0.1.0",
    packages=find_packages(),
    # pip install -e ./app --config-settings editable_mode=compat
    install_requires=[
        "fastapi==0.116.1",
        "uvicorn==0.35.0",
        "numpy==1.26.4",
        "faiss-cpu==1.7.4",
        "langchain==0.3.27",
        "tiktoken==0.9.0",
        "langchain-community==0.3.27",
        "sentence-transformers",
        "langchain-huggingface",
        "langchain-openai==0.3.28",
        "huggingface_hub==0.34.1",
        "google-genai==1.30.0",
        "PyJWT==2.10.1",
        "errorhub==0.1.9",
        "mangum==0.19.0",
    ],
    entry_points={
        "console_scripts": [],
    },
)
