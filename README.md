 # imagegenerator

Welcome to the `imagegenerator` repository, a Python-based application designed for seamlessly compositing images with customizable backgrounds, midgrounds, and foregrounds. This tool can prove beneficial for developers working on projects that require dynamic image manipulation.

## Installation

To get started with the `imagegenerator`, follow these steps:

1. Clone this repository to your local machine using the following command in your terminal or command prompt:

```bash
git clone https://github.com/yourusername/imagegenerator.git
```

2. Navigate into the cloned directory:

```bash
cd imagegenerator
```

3. Install the required packages using pip:

```bash
pip install -r requirements.txt
```

## Usage

After installation, you can use the `main.py` script to generate your composite images. The script takes various command-line arguments that allow you to customize the output image's background (`--background`), midground (`--midground`), and foreground (`--foreground`).

```bash
python main.py --background=path/to/background_image --midground=path/to/midground_image --foreground=path/to/foreground_image --output=path/to/save/output_image
```

By default, the output image will be saved in the `combined_images` folder. You can specify a different location by modifying the `--output` argument.

## File Structure

The repository consists of separate folders for background (`background`), midground (`midground`), and foreground (`foreground`) images, ensuring a modular approach to image management. Additionally, the `combined_images` folder contains the generated composite images.

## Gitignore

In order to keep the virtual environment and temporary files out of version control, we have included a `.gitignore` file in this repository. You can customize it according to your specific project needs.

That's all! We hope you find the `imagegenerator` useful for your projects. If you encounter any issues or have suggestions, please open an issue on this GitHub repository or submit a pull request. Happy image compositing!