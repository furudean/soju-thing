# sojuthing

proxies uploads to [0x0.st](https://0x0.st). it's for a [soju](https://soju.im)
and [senpai](https://git.sr.ht/~delthas/senpai/) setup.

handles the path `/upload` and `/uploads`, expects a form field named `data`
with the file.

there is no authentication. make this available only a trusted network... or
else!

## development

```bash
quart run --reload
```

## deploy

```bash
# build
uv sync  # set up a virtualenv with up to date dependencies
uv build

# on server
pip install dist/*.whl --force
hypercorn sojuthing.main:app
```
