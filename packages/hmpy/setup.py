from distutils.core import setup

setup(
    name='hmpy',
    version='0.3',
    author='Enrique Coronado',
    author_email='enriquecoronadozu@gmail.com',
    url='https://github.com/EmaroLab/HMPy',
    description='Python library for the modelling and recognition of Human Motion Primitives',
    packages=["hmpy", "deep_hmpy"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 2 :: Only",
        "Topic :: Software Development"
    ]
)
