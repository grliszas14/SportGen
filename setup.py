from setuptools import setup

setup(
   name='SportGen',
   version='0.1',
   description='Generator relacji sportowych - projekt na SAG i WEDT',
   author=['Piotr Antosiuk', 'Cezary Modzelewski', 'Grzegorz Wojciechowski'],
   author_email='268960@pw.edu.pl',
   packages=['agents', 'models'],  #same as name
   install_requires=['nltk', 'textblob', 'spade', 'pandas'], #external packages as dependencies
)