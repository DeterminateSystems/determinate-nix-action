Regenerate the readme:

```
./tools/update-state.sh <determinate-nixd version, like v3.5.2>
./tools/generate.sh
```

Before committing, lint your code:

```
ruff format
ruff check
shellcheck ./tools/*.sh
```
