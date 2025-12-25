from setuptools import setup, find_packages

setup(
    name="episode_backend",
    version="0.1.0",
    packages=find_packages(),
    # pip install -e ./app --config-settings editable_mode=compat
    install_requires=[
        # Web framework
        "fastapi==0.116.1",
        "uvicorn==0.35.0",
        # Vector + numeric (Lambda-safe)
        "numpy==1.26.4",
        "faiss-cpu==1.7.4",
        # LangChain core
        "langchain==0.3.27",
        "langchain-community==0.3.27",
        # Gemini embeddings + generation
        "google-genai==1.30.0",
        "langchain-google-genai",
        # Tokenization (safe wheel)
        "tiktoken==0.5.2",
        # Auth / runtime
        "PyJWT==2.10.1",
        "mangum==0.19.0",
        # Logging / error tracking
        "errorhub==0.1.9",
        #aws sdk
        "boto3==1.42.4",
    ],
    entry_points={
        "console_scripts": [],
    },
)
