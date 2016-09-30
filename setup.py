from setuptools import setup


setup(
    name='plankton',
    version='0.1.2',
    description='Plankton - wkhtmltopdf REST service',
    url='https://github.com/django-stars/plankton',
    author='Dmytro Upolovnikov',
    author_email='dmitry.upolovnikov@djangostars.com',
    license='Apache License 2.0',
    packages=['plankton', 'plankton.wkhtmltopdf'],
    scripts=['scripts/plankton-server'],
    download_url = 'https://github.com/django-stars/plankton/tarball/0.1.2',
    keywords=['html to pdf', 'wkhtmltopdf', 'pdf', 'rest'],
    install_requires=['aiohttp==1.0.2', 'Cerberus==0.9.2', 'validators==0.10.1', 'requests==2.10.0'],
    zip_safe=False
)
