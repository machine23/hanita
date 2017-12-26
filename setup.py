from setuptools import setup

setup(
    name="Hanita",
    version='0.1.1',
    description='Simple messenger.',
    long_description='Hanita is simple messenger with multiusers chats.',
    url='https://github.com/machine23/hanita',
    license='MIT',
    keywords=['python', 'messenger', 'hanita'],
    author='Vassili Baranov',
    author_email='vassili.baranov@gmail.com',
    packages=['hanita', 'hanita/forms', 'hanita_server', 'hanita_JIM'],
    include_package_data=True,
    python_requires='>=3.5',
    install_requires=[
        'PyQt5==5.9', 'SQLAlchemy==1.1.15'
    ],
)
