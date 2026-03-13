# imagegenerator

A simple Python tool for compositing images—stack background, midground, and foreground layers into a single output image.

## Installation

```bash
git clone https://github.com/yourusername/imagegenerator.git
cd imagegenerator
pip install -r requirements.txt
```

## Usage

Run `main.py` with paths to your layers:

```bash
python main.py \
  --background=path/to/background.jpg \
  --midground=path/to/midground.png \
  --foreground=path/to/foreground.png \
  --output=path/to/output.jpg
```

- Images are assumed to be the same size. If they differ, they’ll be resized to match the background.
- The `--output` argument is optional; defaults to `combined_images/output.jpg`.

## Directory layout

- `background/` — background images  
- `midground/` — midground images  
- `foreground/` — foreground images  
- `combined_images/` — output folder (created automatically)

## Dependencies

Only one required package: `Pillow`.

## Contributing

Found a bug or have an idea? Open an issue or submit a pull request. Keep changes small and focused.