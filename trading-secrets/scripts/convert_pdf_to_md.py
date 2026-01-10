import argparse
import configparser
import io
import logging
import os
import shutil
from pathlib import Path
from typing import List

import google.generativeai as genai
from dotenv import load_dotenv
from docling.datamodel.document_models import ImageRefMode
from PIL import Image
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    EasyOcrOptions,
    PdfPipelineOptions,
    TesseractCliOcrOptions,
)
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.accelerator_options import AcceleratorDevice, AcceleratorOptions

ASCII_ART = r"""
  ____            _ _     _
 |  _ \  ___   __| (_)_ _| |_
 | | | |/ _ \ / _` | | | | __|
 | |_| | (_) | (_| | | |_| |_
 |____/ \___/ \__,_|_|_|\_|\__|
           PDF to Markdown Converter
               ✨ with Gemini AI ✨
"""

_log = logging.getLogger(__name__)


def describe_image_with_gemini(api_key: str, image_data: bytes, prompt: str) -> str:
    """
    Uses Gemini Pro Vision to generate a description for an image.

    Args:
        api_key: The Google AI API key.
        image_data: The image data in bytes.
        prompt: The prompt to send to the model.

    Returns:
        The generated description or an error message.
    """
    try:
        genai.configure(api_key=api_key)
        img = Image.open(io.BytesIO(image_data))
        model = genai.GenerativeModel("gemini-pro-vision")
        response = model.generate_content([prompt, img])
        return response.text
    except Exception as e:
        _log.error(f"Error calling Gemini API: {e}")
        return "Error generating description."


def convert_pdf_to_markdown(
    pdf_path: Path,
    ocr_engine: str = "easyocr",
    tesseract_path: str | None = None,
    ocr_lang: str | None = None,
    describe_images: bool = False,
    gemini_api_key: str | None = None,
    gemini_prompt: str = "Describe this image in detail, focusing on any text, charts, or data visible.",
):
    """
    Converts a given PDF file to a rich Markdown file using docling.

    The conversion enables OCR and table structure recognition for the best
    possible output from complex documents. The resulting Markdown file is
    saved in the same directory as the source PDF.

    Args:
        pdf_path: The path to the PDF file to be converted.
        ocr_engine: The OCR engine to use ('easyocr' or 'tesseract').
        tesseract_path: Optional path to the Tesseract executable.
        ocr_lang: Optional comma-separated list of languages for OCR.
        describe_images: If True, use Gemini to describe images.
        gemini_api_key: API key for the Gemini model.
        gemini_prompt: The prompt to use for image description.
    """
    if not pdf_path.exists() or pdf_path.suffix.lower() != ".pdf":
        _log.error(f"Error: Invalid or non-existent PDF file at '{pdf_path}'")
        return

    output_md_path = pdf_path.with_suffix(".md")
    _log.info(f"Input PDF: {pdf_path}")
    _log.info(f"Output Markdown will be: {output_md_path}")

    # 1. Configure the pipeline for rich context extraction.
    # Based on your guide, this is ideal for PDFs with images and tables.
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = True  # Enable OCR for text in images
    pipeline_options.do_table_structure = True  # Enable table detection

    # Ensure images are extracted with their data for analysis
    if describe_images:
        pipeline_options.generate_page_images = True
        pipeline_options.generate_picture_images = True

    pipeline_options.table_structure_options.do_cell_matching = True  # Improve table accuracy

    # Add performance optimizations
    pipeline_options.accelerator_options = AcceleratorOptions(
        num_threads=4, device=AcceleratorDevice.AUTO
    )

    # Select the OCR engine based on the argument
    if ocr_engine.lower() == "tesseract":
        # Check for Tesseract executable, prioritizing the provided path
        tesseract_cmd = tesseract_path or shutil.which("tesseract")

        if not tesseract_cmd or not Path(tesseract_cmd).is_file():
            _log.error(
                "Tesseract OCR engine selected, but 'tesseract' command not found."
            )
            _log.error(
                "Please either install Tesseract and add it to your system's PATH,"
            )
            _log.error(
                "or provide the full path to the executable using the --tesseract-path argument."
            )
            _log.error(
                "Official installation guide: https://github.com/UB-Mannheim/tesseract/wiki"
            )
            return  # Exit gracefully if Tesseract is not found

        _log.info(f"Using Tesseract OCR engine at: {tesseract_cmd}")

        ocr_options_kwargs = {"tesseract_cmd": tesseract_cmd}
        if ocr_lang:
            # TesseractCliOcrOptions expects a list of languages
            lang_list = [lang.strip() for lang in ocr_lang.split(",")]
            ocr_options_kwargs["lang"] = lang_list
            _log.info(f"Using Tesseract languages: {lang_list}")

        pipeline_options.ocr_options = TesseractCliOcrOptions(**ocr_options_kwargs)
    else:
        _log.info("Using default EasyOCR engine.")
        if ocr_lang:
            lang_list = [lang.strip() for lang in ocr_lang.split(",")]
            # The default is already EasyOcrOptions, so we can just update the lang
            if isinstance(pipeline_options.ocr_options, EasyOcrOptions):
                pipeline_options.ocr_options.lang = lang_list
            _log.info(f"Using EasyOCR languages: {lang_list}")

    # 2. Create a DocumentConverter with these custom options.
    doc_converter = DocumentConverter(
        format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)}
    )

    # 3. Convert the document.
    _log.info(f"Starting conversion for '{pdf_path.name}'...")
    try:
        conv_result = doc_converter.convert(str(pdf_path))
        _log.info("Conversion successful.")
    except Exception as e:
        _log.error(f"An error occurred during conversion: {e}")
        return

    # 4. Export the result to a Markdown string.
    # We export with referenced images so they are saved to disk and can be linked in the final MD.
    markdown_output = conv_result.document.export_to_markdown(
        image_mode=ImageRefMode.REFERENCED,
        output_path=output_md_path.parent,
        doc_name=output_md_path.stem,
    )

    # 5. Check if the output is empty and log a warning.
    if not markdown_output or not markdown_output.strip():
        _log.warning(
            "Conversion resulted in an empty document. This often means the OCR engine failed to extract text."
        )
        _log.warning("Please review the debug logs below for more details.")
        _log.debug(f"Conversion status: {conv_result.status}")
        _log.debug(f"Conversion error message: {conv_result.error_message}")
        if conv_result.document and conv_result.document.pages:
            _log.debug(f"Number of pages processed: {len(conv_result.document.pages)}")
            # Check if any page has text cells
            has_text_cells = any(
                page.text_cells for page in conv_result.document.pages if page.text_cells
            )
            _log.debug(f"Any page contains text cells: {has_text_cells}")
            if not has_text_cells:
                _log.debug("No text cells found on any page.")
                # Further inspect the first page if it exists
                if conv_result.document.pages: # Ensure there's at least one page
                    first_page = conv_result.document.pages[0]
                    _log.debug(f"First page has {len(first_page.images)} images and {len(first_page.text_cells)} text cells.")
        else:
            _log.debug("No document or pages found in conversion result.")

    # 6. Enhance with Gemini image descriptions if requested
    if describe_images:
        if not gemini_api_key:
            _log.warning(
                "Image description was requested, but no Gemini API key was provided. Skipping."
            )
        else:
            _log.info("Describing images using Gemini Pro Vision...")
            image_descriptions: List[tuple[str, str]] = []
            image_count = 0
            for page in conv_result.document.pages:
                for image in page.images:
                    image_count += 1
                    _log.info(f"  Processing image {image_count}: {image.ref}...")
                    img_data = image.get_image_data()
                    if img_data:
                        description = describe_image_with_gemini(
                            gemini_api_key, img_data, gemini_prompt
                        )
                        image_descriptions.append((image.ref, description))

            if image_descriptions:
                enhancement_section = ["\n\n---\n"]
                enhancement_section.append("## 🖼️ Image Analysis (via Gemini Pro)\n")
                for i, (ref, desc) in enumerate(image_descriptions):
                    enhancement_section.append(f"### Figure {i+1}: `{ref}`\n")
                    enhancement_section.append(f"> **Gemini Description:** {desc}\n")
                markdown_output += "\n".join(enhancement_section)

    # 7. Add a Mermaid diagram of the workflow
    mermaid_diagram = """
---

## ⚙️ Conversion Workflow

```mermaid
graph TD
    A["📄 Input PDF"] --> B{"📚 docling Engine"};
    B -- "Layout & Text" --> C["📝 Core Markdown"];
    B -- "Images" --> D["🖼️ Image Extraction"];
    subgraph "Optional AI Enhancement"
        D --> E{"✨ Gemini Pro Vision"};
        E --> F["🤖 AI Descriptions"];
    end
    C & F --> G["🧩 Final Markdown Assembly"];
    G --> H["📜 Output.md"];

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style H fill:#ccf,stroke:#333,stroke-width:2px
```
"""
    if describe_images:
        markdown_output += mermaid_diagram

    # 8. Save the final Markdown file.
    try:
        with open(output_md_path, "w", encoding="utf-8") as fp:
            fp.write(markdown_output)
        _log.info(f"Successfully saved rich Markdown to: {output_md_path}")
    except Exception as e:
        _log.error(f"Failed to save Markdown file: {e}")


def main():
    """Main function to parse command-line arguments and run the conversion."""
    # Load environment variables from .env file, if it exists.
    load_dotenv()

    print(ASCII_ART)

    parser = argparse.ArgumentParser(
        description="Convert a PDF file to a rich Markdown file using docling, with optional Gemini AI enhancements.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "pdf_file", type=str, help="The path to the PDF file to convert."
    )
    parser.add_argument(
        "--ocr-engine",
        type=str,
        choices=["easyocr", "tesseract"],
        default="easyocr",
        help="Specify the OCR engine to use. 'tesseract' requires system installation.",
    )
    parser.add_argument(
        "--tesseract-path",
        type=str,
        default=None,
        help="Specify the full path to the tesseract.exe executable if it's not in the system PATH.",
    )
    parser.add_argument(
        "--ocr-lang",
        type=str,
        default=None,
        help="Comma-separated list of languages for the OCR engine (e.g., 'eng,fra').",
    )
    parser.add_argument(
        "--describe-images",
        action="store_true",
        help="Enable image description using Google Gemini Pro Vision.",
    )
    parser.add_argument(
        "--gemini-api-key",
        type=str,
        default=None,
        help="Google AI API key for Gemini. Overrides the key in the config file.",
    )
    parser.add_argument(
        "--gemini-prompt",
        type=str,
        default="Describe this image in detail, focusing on any text, charts, or data visible.",
        help="The prompt to use for image description with Gemini.",
    )
    parser.add_argument(
        "--config",
        default="config.ini",
        help="Path to the configuration file (default: config.ini).",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase verbosity level. -v for INFO, -vv for DEBUG.",
    )
    args = parser.parse_args()

    # Setup logging based on verbosity
    log_level = logging.WARNING
    if args.verbose == 1:
        log_level = logging.INFO
    elif args.verbose >= 2:
        log_level = logging.DEBUG

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        force=True,  # Re-configure the root logger
    )

    # Read API key from config file
    config = configparser.ConfigParser()
    api_key_from_config = None
    try:
        if Path(args.config).exists():
            config.read(args.config)
            # Check if a non-placeholder key exists in the config
            config_key = config.get("gemini", "api_key", fallback=None)
            if config_key and "YOUR_API_KEY" not in config_key and config_key.strip():
                api_key_from_config = config_key
                _log.warning(
                    f"API key found in '{args.config}'. For better security, "
                    "it is recommended to use a .env file or set the GEMINI_API_KEY environment variable."
                )
    except configparser.Error as e:
        _log.warning(f"Could not parse config file '{args.config}': {e}")

    # Prioritize key from: 1. CLI argument, 2. Environment variable, 3. Config file
    final_gemini_key = (
        args.gemini_api_key or os.getenv("GEMINI_API_KEY") or api_key_from_config
    )

    convert_pdf_to_markdown(
        Path(args.pdf_file),
        ocr_engine=args.ocr_engine,
        tesseract_path=args.tesseract_path,
        ocr_lang=args.ocr_lang,
        describe_images=args.describe_images,
        gemini_api_key=final_gemini_key,
        gemini_prompt=args.gemini_prompt,
    )


if __name__ == "__main__":
    main()