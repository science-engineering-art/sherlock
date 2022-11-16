# Information Retrieval Systems

## Installation

### Python

```shell
pip install fastapi
pip install "uvicorn[standard]"
pip install unidecode
pip install ir_datasets
```

### React

```shell
cd src/client
npm install
```

## Execution

### Linux

From the root directory run in a terminal,

```shell
make python
```

and run this in another terminal.

```shell
make react
```

### Windows

From the root directory run in a terminal,

```shell
cd src
uvicorn main:app --reload
```

and run this in another terminal.

```shell
cd src/client
npm start
```

Finally, enter the browser at the following web address [localhost:3000](http://localhost:3000).
