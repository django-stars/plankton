from setuptools import setup
from pip.req import parse_requirements


install_reqs = parse_requirements('requirements.txt', session=False)
reqs = [str(ir.req) for ir in install_reqs]

setup(name='plankton',
      version='0.1',
      description='Plankton - wkhtmltopdf REST service',
      url='https://github.com/django-stars/plankton',
      author='Dmytro Upolovnikov',
      author_email='dmitry.upolovnikov@djangostars.com',
      license='Apache License 2.0',
      packages=['plankton', 'plankton.wkhtmltopdf'],
      scripts=['scripts/plankton-server'],
      install_requires=reqs,
      zip_safe=False)
