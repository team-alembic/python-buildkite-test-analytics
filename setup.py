from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='buildkite-test-analytics',
      version='0.0.1',
      description='Buildkite Test Analytics',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/team-alembic/python-buildkite-test-analytics',
      author='James Harton',
      author_email='james.harton@alembic.com.au',
      license='MIT',
      classifiers=[
          "License :: OSI Approved :: MIT",
      ],
      py_modules=['bkta'],
      zip_safe=False,
      package_dir={'': 'src'},
      extras_require={
          "dev": [
              "pytest>=7",
              "mock>=4",
              "check-manifest",
              "twine"
          ]
      })
