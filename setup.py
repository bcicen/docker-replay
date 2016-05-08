from setuptools import setup

exec(open('rerun/version.py').read())

setup(name='docker-rerun',
      version=version,
      packages=['rerun'],
      description='Generate docker run commands from running containers',
      author='Bradley Cicenas',
      author_email='bradley.cicenas@gmail.com',
      url='https://github.com/bcicen/docker-rerun',
      install_requires=['docker-py>=1.7.2'],
      license='http://opensource.org/licenses/MIT',
      classifiers=(
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License ',
          'Natural Language :: English',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.4',
      ),
      keywords='docker docker-py devops',
      entry_points = {
        'console_scripts' : ['docker-rerun = docker_rereun:main']
      }
)
