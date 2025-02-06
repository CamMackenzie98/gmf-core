from setuptools import setup, find_packages

setup(
    name='gmf',
    version='0.1',
    packages=find_packages('./gmf'),
    install_requires=[
    ],
    entry_points={
        #'console_scripts': [
        #    'run_bathy=empbathy.core.process:cli',# Maps the bathy command to run the script
        #    'bathy_dockerentry=empbathy.tools.docker:main',  # Maps the bathy_docker command to run the script
        #],
    },
)