from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()
setup(
    name='TooFastAndNotFurious',
    version='1.0.0',
    description='Traffic simulator',
    long_description=readme,
    author='Olivier Boulet, Thomas Canava, Thibaut Gonnin, Jeremy Junac',
    author_email='olivier.boulet@etu.unice.fr, thomas.canava@etu.unice.fr, thibaut.gonnin@etu.unice.fr, jeremy.junac@etu.unice.fr, ',
    url='https://mjollnir.unice.fr/bitbucket/projects/PNSD/repos/main/',
    packages=find_packages()
)