
# Elden Brain

Elden Brain is a tool for generating an [Obsidian Vault](https://obsidian.md/) containing pages for (almost) everything in Elden Ring. Obsidian is not only a great note-taking application, it also features a graph view that visualizes connected pages, allowing for unique insights into Elden Ring's elaborate interconnected world.

This tool is intended give any lore hunter a starting part in their investigations and theories, or simply for players to use as a local reference as they play the game.

## Installation

Install using the included Wheel

```bash
  pip install eldenbrain-<version>-py3-none-any.whl
```

Alternatively, download this repository and install using Poetry

```bash
poetry install
```

Following installation, run the 'eldenbrain' command and follow the prompts to get started.

## Features

- Automatic Obsidian Vault generation
- CLI included, or can be used as a Python library
- Extensive formatting options via configuration file

## Usage/Examples

### Running from the command line
If you wish to skip the details and create the entire Vault, type
```bash
eldenbrain create --all
```
For a more granular experience, pages can be created individually, or by category. To see the available categories, type
```bash
eldenbrain list
```
To see the names of all pages within that category (without yet creating them), type
```bash
eldenbrain list --category "Creatures and Enemies"
```
To create all pages within a category, type
```bash
eldenbrain create --category "Creatures and Enemies"
```
Or create a single page if you know the name (Note: A category is not required in this case, but omitting one will create the page at the Vault's top level)
```bash
eldenbrain create Troll -c "Creatures and Enemies"
```

By default, the Vault will be created in the installation directory in a folder named **cache/Elden Ring/**. This path can be changed in config.ini.

Note: It is **highly** recommended that the included Obsidian settings file be used with your project. This configures the settings in Obsidian's graph view for the recommended Elden Brain experience. In order to use it, drop the included .obsidian folder in the local Vault folder after creation. That's it!

### Importing as a Python library

Elden Brain can be imported as a Python library with the following statement:

```python
from eldenbrain import EldenBrain as eb
```

## Bandwidth considerations

Elden Brain works by scraping information from the web to generate Markdown pages. Please be thoughtful and considerate of bandwidth when using this tool—keep your use of create --all to a minimum, test your config.ini changes by creating a single page, etc.

By default, downloaded assets (namely images) are *not* re-downloaded when a local page is recreated.