from os import path
from setuptools import setup, find_packages

# Caminho base do projeto
here = path.abspath(path.dirname(__file__))

# Lê o README (para descrição longa)
with open(path.join(here, 'README.md'), encoding='utf-8') as readme_file:
    readme = readme_file.read()

# Lê a versão do projeto
with open(path.join(here, 'VERSION'), encoding='utf-8') as version_file:
    version = version_file.read().strip()

# Lê as dependências do projeto
with open(path.join(here, 'requirements.txt')) as requirements_file:
    requirements = [
        line.strip()
        for line in requirements_file
        if line.strip() and not line.startswith('#')
    ]

# Configuração do pacote
setup(
    name="prj_BuscaEstabelecimento",
    version=version,
    description="Realiza a coleta de dados no Google",
    long_description=readme,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=['docs', 'tests']),
    include_package_data=True,
    install_requires=requirements,
)
