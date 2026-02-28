# Episode-Clone

A project for creating interactive story experiences similar to Episode.

## Virtual Environment

### Creating a virtual environment (if not already created)

```bash
python3 -m venv .venv
```

### Activating the virtual environment

```bash
source .venv/bin/activate
```

### Deactivating the virtual environment

```bash
deactivate
```

### Verifying you are in the virtual environment

Check if the virtual environment is active:

```bash
echo $VIRTUAL_ENV
```

or

```bash
which python
```

If inside a venv, `$VIRTUAL_ENV` will show the path to your `.venv` directory, and `which python` will point to `.venv/bin/python`.

## Getting Started

1. Create and activate the virtual environment (see above)
2. Install dependencies:
   ```bash
   pip install -e ./episode
   ```
3. Run the application:
   ```bash
   cd episode
   uvicorn main:episode --reload
   ```

## Development

This project runs in a dev container. See `.devcontainer/devcontainer.json` for configuration details.

architect → developer → tester → reviewer → done
