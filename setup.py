import os
import sys

from setuptools import find_packages,setup
from typing import List

def get_requirements()->List[str]:
    '''This fundction will return lsit of requirements'''
    requirement_lst:List[str]=[]
    try:
        with open('requirements.txt','r') as file:
            lines=file.readlines()
            for line in lines:
                requirement=line.strip()
                if requirement and requirement != '-e .':
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print("requirement.txt file not found")

    return requirement_lst

setup(
    name="Network Security",
    version="0.0.1",
    author="Harsh Verma",
    author_email="jsrharshverma@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)        
