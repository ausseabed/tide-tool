from setuptools import setup, find_packages

setup(
    name='tide-tool',
    namespace_packages=['tidetool'],
    version='0.0.1',
    url='https://github.com/ausseabed/tide-tool',
    author=(
        "Lachlan Hurst;"
    ),
    author_email=(
        "lachlan.hurst@gmail.com;"
    ),
    description=(
        "Command line utility for updating CARIS zone definition files with "
        "tide data predicted by the AVISO-FES model"
    ),
    entry_points={
        "gui_scripts": [],
        "console_scripts": [
            'tidetool = tidetool.tidetool:main',
        ],
    },
    packages=[
        'tidetool',
        'tidetool.lib'
    ],
    zip_safe=False,
    package_data={},
    install_requires=[
        'Click'
    ],
    tests_require=['pytest'],
)
