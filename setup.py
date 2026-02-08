from setuptools import find_packages, setup
from typing import List

HYPEN_E_DOT='-e .'
def get_requirements(file_path: str) -> List[str]:
    """
    This function will return the list of requirements
    It reads the requirements from the file specified by the file_path parameter
    and returns the list of requirements.
    """
    requirements = []
    with open(file_path) as file_obj:
        # Read the lines from the file
        requirements = file_obj.readlines()
        # Remove the newline character from each requirement
        requirements = [req.replace("\n", "") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    return requirements

setup(
    name="mlproject",
    version='0.0.1',
    author='Nihal',
    authour_email='nihaljaisawal1@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
    # install_requires=['pandas','numpy',....]

)