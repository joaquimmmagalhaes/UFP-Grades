# UFP-Grades

UFP-Grades is a system to auto-notify new grades available for Fernando Pessoa University.

# Features!

  - Notify by email
  - Notify by Pushbullet.
  - Notify by SMS using BulkSMS.
  - Multi-threaded (faster analisys)
  - Two Web Scrapers
  - Fast as hell

### Installation

UFP-Grades requires [Python](https://www.python.org/) v3+, [MySQL](https://www.mysql.com) and [PhantomJS](http://phantomjs.org) to run.


### Usage

```sh
$ git clone https://github.com/joaquimmagalhaes17/UFP-Grades.git
$ cd UFP-Grades
$ cp .config.yml.example .config.yml
$ nano .config.yml 
Fill the yaml file with your configurations
$ pip3 install -r requirements.txt
$ python3 grades.py
Or
$ python3 grades.py -a <number> <password> <email>
```

# This system also requires [UFP-API](https://github.com/rafaelcpalmeida/UFP-API)

### Todos
 - Document code

### Special thanks to:
- [Rafael Almeida](https://github.com/rafaelcpalmeida) for creating the API
- Pedro Monteiro

# MIT License
**Free Software, Hell Yeah!**