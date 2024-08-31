from __future__ import annotations

from setuptools import find_packages
from setuptools import setup

setup(
    name='statikk',
    version='0.1.0',
    description='An open-source Firebase alternative built with Python and SurrealDB',
    # Finds all packages under the src directory
    packages=find_packages(where='src'),
    package_dir={'': 'src'},  # Sets the package directory to src
    include_package_data=True,  # Includes data from MANIFEST.in
    install_requires=[
        'fastapi',
        'uvicorn',
        'pydantic',
        'tortoise-orm',
        'passlib',
        'python-jose',
        'aiofiles',
    ],
    extras_require={
        'dev': [
            'pytest',
            'pytest-cov',
            'flake8',
            'mypy',
            'pre-commit',
            # Add other development dependencies here
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        # Add other relevant classifiers
    ],
    python_requires='>=3.8',
)
