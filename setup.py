from setuptools import setup

setup(
    name="Hanita",
    version='0.1.3',
    description='Simple messenger.',
    long_description='Hanita is simple messenger with multiusers chats.',
    url='https://github.com/machine23/hanita',
    license='MIT',
    keywords=['python', 'messenger', 'hanita'],
    author='Vassili Baranov',
    author_email='vassili.baranov@gmail.com',
    packages=[
        'hanita',
        'hanita/forms',
        'hanita/forms/templates',
        'hanita_server',
        'hanita_server/avatars',
        'hanita_JIM',
    ],
    package_data={
        '': ['default_avatar.png', 'template.html'],
    },
    include_package_data=True,
    python_requires='>=3.5',
    install_requires=[
        'PyQt5==5.9',
        'SQLAlchemy==1.1.15',
        'Jinja2==2.11.3',
        'Pillow==5.0.0',
        'PyOpenGL==3.1.0',
        'pymongo==3.6.0',
    ],
)
