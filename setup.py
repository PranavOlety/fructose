from setuptools import setup

setup(
    name='fructose',
    version='0.0.5',
    packages=["fructose"],
    package_dir={'': 'src'},
    install_requires=[
        'openai',
        'Jinja2'
    ],
    # Additional metadata about your package
    author='Banana',
    author_email='erik@banana.dev',
    description='A package for strongly-typed LLM function calling',
    url='https://github.com/bananaml/fructose',
)
