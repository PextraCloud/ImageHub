# Pextra ImageHub™

[![Release](https://github.com/PextraCloud/ImageHub/actions/workflows/cd.yml/badge.svg)](https://github.com/PextraCloud/ImageHub/actions/workflows/cd.yml)

### Access the image library [in the Pextra CloudEnvironment® web UI](https://docs.pextra.cloud/TODO) or visit [ImageHub™ directly](https://imagehub.pextra.cloud/).
### If you would like to request an image, please [open an issue](https://github.com/PextraCloud/ImageHub/issues) or [start a discussion](https://github.com/PextraCloud/ImageHub/discussions).
---

ImageHub™ provides a curated list of instance images for [Pextra CloudEnvironment®](https://pextra.cloud/products/cloudenvironment), for a one-click deployment experience of your favorite operating systems and applications.

**Note**: Images provided by ImageHub™ may be used on other private or public cloud platforms, but the deployment experience may vary. Only use with Pextra CloudEnvironment® is supported.

## Development

A simple Python script is provided to generate the image library from the source files. A GitHub workflow also automatically runs to generate the image library upon pushes to `master`, creating a new release.

### Dependencies
- Python 3.6 or higher
- `requests` library

### Steps
1. Clone this repository.
2. Install the `requests` library by running `pip install requests`.

### Running
1. Run `python main.py` to start the program. It will read source files from the `sources` directory.
2. The generated image library will be saved to `output/library.json`.

## Support/Contact

For enterprise licensing, support, and consulting, please visit [our website](https://pextra.cloud/enterprise). Alternatively, you can contact us at [enterprise@pextra.cloud](mailto:support@pextra.cloud).

If you have any questions, please feel free to open an issue or a discussion. You can also contact us at [support@pextra.cloud](mailto:support@pextra.cloud).

## Contributions

We welcome contributions! If you find any bugs, have feature requests, or would like to contribute enhancements, please feel free to open issues or submit pull requests.

## License

ImageHub™ is licensed under the [Apache License 2.0](LICENSE).

