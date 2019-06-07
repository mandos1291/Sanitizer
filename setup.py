import setuptools

setuptools.setup(
    name="sanitizer",
    version="1.0",
    author="Matthias Christe",
    author_email="matthias.christe@hefr.ch",
    description="GSW LID using TensorFlow, LSTM-based",
    license='Apache License 2.0',
    long_description="This module sanitizer allow to parse a file of text and to sanitize with fixed rules. The goal is to process a text in different ways before using it in a data science project. Machine learning is one field that often need to sanitize the text.",

    packages=setuptools.find_packages(),
    #package_data={'': ['*.fasttext*']},  # include yaml and pickle from any module
    entry_points={
        'console_scripts': [
            'sanitizer = sanitizer.__main__:main',
        ]
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: Apache 2.0 License",
        "Operating System :: OS Independent",
    ),
    install_requires=[
        'click==7.0'
    ]
)
