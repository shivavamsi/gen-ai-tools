# Python Library Documentation

## Docstring Style (Google)

```python
def encode(latitude: float, longitude: float, *, precision: int = 12) -> str:
    """Encode geographic coordinates to a quadtree string.

    Args:
        latitude: The latitude in degrees (-90 to 90).
        longitude: The longitude in degrees (-180 to 180).
        precision: Number of characters in output. Defaults to 12.

    Returns:
        A string representing the encoded location.

    Raises:
        ValidationError: If coordinates are out of valid range.

    Example:
        >>> encode(37.7749, -122.4194)
        '9q8yy9h7wr3z'
    """
```

## Sphinx Quick Setup

```bash
# Install
uv add --dev sphinx furo myst-parser sphinx-copybutton

# Initialize
sphinx-quickstart docs/
```

**conf.py essentials:**
```python
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',  # Google docstrings
    'myst_parser',          # Markdown support
]
html_theme = 'furo'
```

## pyproject.toml Dependencies

```toml
[project.optional-dependencies]
docs = [
    "sphinx>=7.0",
    "furo>=2024.0",
    "myst-parser>=2.0",
]
```

## README Template

```markdown
# Package Name

[![PyPI](https://badge.fury.io/py/package.svg)](https://pypi.org/project/package/)

Short description of what it does.

## Installation

uv add package

## Quick Start

from package import function
result = function(args)

## Documentation

Full docs at [package.readthedocs.io](https://package.readthedocs.io/)
```

## ReadTheDocs (.readthedocs.yaml)

```yaml
version: 2

build:
  os: ubuntu-24.04
  tools:
    python: "3.12"
  jobs:
    install:
      - asdf plugin add uv
      - asdf install uv latest
      - asdf global uv latest
      - uv sync --extra docs
    build:
      html:
        - uv run sphinx-build -W -b html docs $READTHEDOCS_OUTPUT/html

sphinx:
  configuration: docs/conf.py
```

Driving the build through uv makes RTD use the same environment as local
development. See **[documentation-sphinx-config.md](documentation-sphinx-config.md)**
for the annotated version.

For detailed setup, see:
- **[documentation-sphinx-config.md](documentation-sphinx-config.md)** - Full Sphinx configuration
- **[documentation-tutorials.md](documentation-tutorials.md)** - Tutorial writing guide

## Checklist

```
README:
- [ ] Clear project description
- [ ] Installation instructions
- [ ] Quick start example
- [ ] Link to full documentation

API Docs:
- [ ] All public functions documented
- [ ] Args, Returns, Raises sections
- [ ] Examples in docstrings
- [ ] Type hints included
```
