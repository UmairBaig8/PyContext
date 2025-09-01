from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="pycontext-workflow",
    version="1.0.0",
    author="PyContext Contributors",
    author_email="your.email@example.com",
    description="A professional workflow engine with priority-based execution and checkpoint resumption",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pycontext",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Distributed Computing",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-asyncio>=0.18.0",
            "black>=22.0",
            "flake8>=4.0",
            "mypy>=0.950",
        ],
    },
    entry_points={
        "console_scripts": [
            "pycontext-demo=main_layered:main",
        ],
    },
    keywords="workflow, engine, priority, checkpoint, async, orchestration",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/pycontext/issues",
        "Source": "https://github.com/yourusername/pycontext",
        "Documentation": "https://github.com/yourusername/pycontext/docs",
    },
)