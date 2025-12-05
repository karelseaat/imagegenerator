 # imagegenerator

Welcome to the `imagegenerator` repository, a Python-based application for compositing images with customizable backgrounds, midgrounds, and foregrounds. This tool can benefit developers working on projects requiring dynamic image manipulation.

## Installation

To get started with the `imagegenerator`, follow these steps:

1. Clone this repository to your local machine using the command below in your terminal or command prompt:

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

## Code Structure

The application's logic resides within the `main.py` script. The code first loads images from their respective folders and performs necessary operations such as colorization, alignment, and resizing before combining them into a final composite image.

## Dependencies

The following dependencies are required to run this application:

- Pillow (PIP package)

## Contributing

If you encounter any issues or have suggestions, please open an issue on the [Issues](https://github.com/yourusername/imagegenerator/issues) tab of this repository. We welcome pull requests as well!

## License

This project is licensed under the MIT License - see the LICENSE file for details.

That's all! We hope you find the `imagegenerator` useful for your projects. Enjoy coding!