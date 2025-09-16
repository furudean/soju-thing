# soju thing

proxies uploads to [0x0.st](https://0x0.st). it's for a [soju](https://soju.im)
and [senpai](https://git.sr.ht/~delthas/senpai/) setup.

handles the path `/upload` and `/uploads`, expects a form field named `data`
with the file.

there is no authentication. make this available only a trusted network... or
else!

## development

```
quart run --reload
```

## deploy

i don't know yet...
