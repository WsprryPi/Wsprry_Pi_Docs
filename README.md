# Wsprry Pi Documentation

The documents are written in Markdown with Sphinx and hosted on Read the Docs (RTD) and accessible via [wsprdocs.aa0nt.net](http://wsprdocs.aa0nt.net/).

## RTD Documentation Labels

Three labels are maintained and automatically built by RTD:

- `stable`: Built from the latest released version
- `latest`: Built from the default branch (`main`), but not guaranteed to be a release and can be ahead of `stable`.
- `devel`: Build from the devel branch, and generally considered in development along side it's corresponding code.

## Working with the Docs

First, create a virtual environment:

``` bash
cd docs
sudo apt install python3-venv -y
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Or you can use the `create_venv.sh` script provided.

Now you have the requirements:

- `sphinx`
- `sphinx_rtd_theme`
- `myst-parser`
- `esbonio`
- `requests`

From here you can `make html` to create the docs in `./build/html`.

You can also use the release script `copy_docs.sh` to copy the documentation to your local webserver at `wsprrypi/docs`.
