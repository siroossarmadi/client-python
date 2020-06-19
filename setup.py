from setuptools import find_packages, setup

setup(
    name='gimulator-client',
    description='Python client for Gimulator',
    url='https://github.com/Gimulator/client-python',
    email='siroos.sarmadi@gmail.com',
    author='Siroos Sarmadi',
    requiers_python='>=3.6.0',
    version='0.1.0',
    packages=find_packages(),
    license='MIT',
    install_requires=[
        "requests==2.23.0",
        "websocket-client==0.57.0"
    ]
)
