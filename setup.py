#!/usr/bin/env python

from distutils.core import setup

setup(name="OperonDB",
	version="2.0",
	description="Tools for dealing with operon databases, including my own.",
	author="Bryan Lunt",
	author_email="lunt@ctpb.ucsd.edu",
	url="http://matisse.ucsd.edu/~lunt/amaranth",
	package_dir={'':'src'},
	packages=["operondb","operondb.imp","operondb.imp.lunt",],
	requires=["SQLAlchemy (>=0.8.0)"],
	classifiers=["Intended Audience :: Bioinformaticians"]
)
