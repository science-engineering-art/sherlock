# Informational Retrieval Systems
[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg?label=license)](https://opensource.org/licenses/MIT) [![Last commit](https://img.shields.io/github/last-commit/science-engineering-art/sherlock.svg?style=flat)](https://github.com/science-engineering-art/sherlock/commits) [![GitHub commit activity](https://img.shields.io/github/commit-activity/m/science-engineering-art/sherlock)](https://github.com/science-engineering-art/sherlock/commits) [![Github Stars](https://img.shields.io/github/stars/science-engineering-art/sherlock?style=flat&logo=github)](https://github.com/science-engineering-art/sherlock) [![Github Forks](https://img.shields.io/github/forks/science-engineering-art/sherlock?style=flat&logo=github)](https://github.com/science-engineering-art/sherlock) [![Github Watchers](https://img.shields.io/github/watchers/science-engineering-art/sherlock?style=flat&logo=github)](https://github.com/science-engineering-art/sherlock) [![GitHub contributors](https://img.shields.io/github/contributors/science-engineering-art/sherlock)](https://github.com/science-engineering-art/sherlock/graphs/contributors)

<center><img src="media/frontend.jpg"/></center>

Sherlock is a search engine developed by computer science students for purely academic purposes. Any kind of contribution to the project is welcome.

## Installation

```shell
make install
```

## Execution

From the root directory run in a terminal,

```shell
make python
```

and run this in another terminal.

```shell
make react
```

## Docker

You may not want to conflict with packages installed on your local computer, you can more easily build the docker image and run it with a container.

From the root directory runs from a terminal to lift the service,

```shell
make run-docker
```

and to close the service.

```shell
make stop-docker
```

Finally, enter the browser at the following web address [localhost:3000](http://localhost:3000).
