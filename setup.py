from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='buildkite-test-collector',
      version='0.0.1',
      description='Buildkite Test Analytics collector',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/team-alembic/python-buildkite-test-analytics',
      author='James Harton',
      author_email='james.harton@alembic.com.au',
      license='MIT',
      classifiers=[
          "License :: OSI Approved :: MIT",
      ],
      py_modules=['buildkite_test_collector'],
      zip_safe=False,
      package_dir={'': 'src'},
      install_requires=["requests>=2"],
      extras_require={
          "dev": [
              "pytest>=7",
              "mock>=4",
              "check-manifest",
              "twine",
              "responses",
          ]
      })
