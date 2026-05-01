# Artfetch

## Table of contents

*   [Overview](#overview)
*   [Requirements](#requirements)
*   [Directory structure](#directory-structure)
*   [Setup](#setup)
*   [Usage](#usage)
*   [Options](#options)
    *   [Rendering](#rendering)
    *   [Display](#display)
*   [Output](#output)
*   [License](#license)
*   [Acknowledgments](#acknowledgments)

## Overview

Artfetch is a modular, agnostic framework for generating, managing, and displaying custom high-quality ANSI art in Linux terminal every time a new shell is opened.

## Requirements

- [**Python 3.6+**](https://www.python.org/downloads/) and dependencies for running the scripts.
- [**Chafa 1.8.0**](https://github.com/hpjansson/chafa/) for image-to-text conversion.

## Directory structure

```text
.
├── assets
│   └── example.png             # Example terminal display
├── examples
│   └── heraldry                # Example category directory
│       ├── ch_cantons.json     # Example collection configuration file
│       └── ...
├── process_images.py           # Script to process images
├── README.md                   # This README file
└── setup.py                    # Script to create or update the base framework
```

## Setup

**1. Clone the repository**

Clone this repository.

```bash
$ git clone https://github.com/dmgtorres/artfetch.git
```

**2. Initialize the base framework**

Run the setup script. This creates the hidden `~/.artfetch/` directory and generates the universal `display.sh` script.

```bash
$ python setup.py
```

To update the display framework at any time, edit the `setup.py` script and run it again.

**3. Add the display script to shell profile**

To display a random piece of art every time a new shell terminal is opened, add the `setup.py` script to the `~/.bashrc` or `~/.zshrc` script.

```bash
~/.artfetch/display.sh ~/.artfetch
```

## Usage

To create or update an art collection, follow these steps.

**1. Prepare a JSON configuration file**

Create a JSON file (e.g., `heraldry/ch_cantons.json`) with the metadata for the desired category, collection, rendering options, and images.

**Example JSON file**

```json
{
    "category": "heraldry",
    "category_name": "Heraldry",
    "collection": "ch_cantons",
    "collection_name": "Cantons of Switzerland",
    "prefix": "ch",
    "resolution": "30x30",
    "rendering_options": "--symbols=block",
    "items": [
        {
            "id": "AG",
            "name": "Aargau",
            "source_type": "wikimedia",
            "source_path": "Wappen_Aargau_matt.svg"
        }
        ...
    ]
}
```

**Note:** `source_type` can be `"wikimedia"` (uses smart API fetching) or `"direct_url"` (standard download).

**2. Generate arts**

Run the processing script by passing the JSON configuration file. It will download the images, convert them to `.ansi` files using Chafa, embed the display name as the first line, and save them in the corresponding directory.

```bash
$ python process_images.py <category>/<collection>.json
```

To update the generated images at any time, edit the `<category>/<collection>.json` file and run the script again.

## Options

### Rendering

The rendering style of a collection can be defined by modifying the `"rendering_options"` value in the corresponding JSON file before generating the items. This works by passing the string as options for Chafa. Therefore, only a combination of Chafa options is valid.

Chafa supports multiple output formats ranging from modern native pixels to retro ASCII.

#### 1. Formats

- **`--format=symbols` (default)**: Renders using ASCII, Braille, and Unicode blocks. Compatible with almost all terminals.
- **`--format=sixel`**: Renders full-resolution native image pixels. Supported by xterm, iTerm2, foot, and Alacritty.
- **`--format=kitty`**: Renders full-resolution native image pixels using the Kitty graphics protocol (Kitty, WezTerm).
- **`--format=iterm`**: Renders native pixels for iTerm2 and WezTerm.

#### 2. Symbol styles

When rendering in text mode (`--format=symbols`), the characters that Chafa uses to draw the image can be controlled using the `--symbols` option:

- **`--symbols=block`**: Uses half and quarter Unicode blocks. Best for bright colors and clean, dense images.
- **`--symbols=braille`**: Uses Braille dot patterns. Excellent for capturing fine geometric lines, curves, and high-detail contours.
- **`--symbols=ascii`**: Uses pure retro ASCII (letters, numbers, and punctuation).
- **`--symbols=vhalf`**: Uses only vertical half-blocks. Creates a very sharp, "8-bit/16-bit Nintendo" pixel art aesthetic.

#### 3. Color and dithering options

- **`--colors=full` (default)**: True 24-bit RGB color.
- **`--colors=256` or `16` or `none`**: Restricts the palette for a retro computing look. 
- **`--dither=none`**: Disables color blending. Combine this with `--symbols=vhalf` or `--symbols=block` for a harsh, distinct pixel-art aesthetic.
- **`--invert`**: Swaps the foreground and background mapping. Helpful for pure ASCII rendering on light terminal themes.

#### Example configurations

*   **Modern block art (default):** `"--format=symbols --symbols=block"`
*   **True high-resolution native image (requires Kitty/WezTerm):** `"--format=kitty"`
*   **8-Bit pixel art:** `"--format=symbols --symbols=vhalf --dither=none"`
*   **Pure 1980s monochrome ASCII:** `"--format=symbols --symbols=ascii --colors=none --invert"`

For a complete list of commands, advanced dithering controls, and font-ratio adjustments, refer to the [official Chafa Man Page](https://hpjansson.org/chafa/man/).

### Display

#### Display all categories

To randomize across all categories, point the script at the top level. This is the option suggested in [Setup](#setup).

```bash
~/.artfetch/display.sh ~/.artfetch
```

#### Display all collections from a specific category

To randomize across all collections in a specific category, point the script one level up.

```bash
~/.artfetch/display.sh ~/.artfetch/<category>
```

#### Display a specific collection

To only show a specific collection, point it directly at its directory.

```bash
~/.artfetch/display.sh ~/.artfetch/<category>/<collection>
```

## Output

This framework isolates the display script from the art library. The ANSI files are organized into a `{Category name} > {Collection name}` hierarchical structure.

**Example directory structure**

```text
~/.artfetch/
├── display.sh              # Display engine
├── heraldry/               # Example category
│   └── ch_cantons/         # Example collection
│       ├── ch_ag.ansi      # Example item raw text file containing ANSI art
│       └── ...
└── ...
```

The output in the terminal should be as follows:

```bash
{Category name} > {Collection name}: {Image title}

[ART HERE]

$
```

**Example terminal display**

![Terminal display with default rendering style](example.png)

## License

The source code for this project is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

## Acknowledgments

*   Diogo Torres <<diogomtorres30@gmail.com>>
