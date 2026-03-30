import argparse
import warnings
import fitz  # PyMuPDF
import os
import re
import sys

# Optional import for fallback functionality
try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False

warnings.warn("Execution started")

class CheckPdfTypeOptions:
    def __init__(self, file_path):
        self.file_path = file_path
        _, file_extension = os.path.splitext(self.file_path)
        self.input_file_type = file_extension.lstrip('.').lower()

class CheckPdfTypeProcessor:
    class PdfType:
        DIGITAL = "Digital"
        SCANNED = "Scanned"

    def __init__(self, pdf_options: CheckPdfTypeOptions):
        self.pdf_options = pdf_options

    def process(self) -> str:
        self.check_if_pdf()
        return self.detect_pdf_type()

    def check_if_pdf(self):
        if self.pdf_options.input_file_type != 'pdf':
            raise ValueError("File not supported: only PDF files are allowed.")

    @staticmethod
    def is_junk_text(text: str) -> bool:
        if not text or len(text.strip()) < 20:
            return True
        text = text.strip()
        # CID-like patterns
        cid_matches = re.findall(r'\(cid:\d+\)', text)
        if len(cid_matches) > 10:
            return True
        # ASCII vs non-ASCII
        ascii_chars = sum(1 for c in text if 32 <= ord(c) <= 126)
        non_ascii_chars = len(text) - ascii_chars
        non_ascii_ratio = non_ascii_chars / len(text)
        if non_ascii_ratio > 0.3:
            return True
        # Low word count
        if len(text.split()) < 10:
            return True
        # Symbol-only bias
        punct_chars = sum(1 for c in text if c in "(){}[]<>/\\|")
        if punct_chars / len(text) > 0.4:
            return True
        return False

    def detect_pdf_type(self) -> str:
        try:
            page_scores = []
            with fitz.open(self.pdf_options.file_path) as doc:
                for pageno in range(doc.page_count):
                    page = doc[pageno]
                    text = page.get_text("text").strip()
                    images = page.get_images(full=True)
                    text_blocks = page.get_text("blocks")
                    bbox = page.rect

                    # --- Text quality check ---
                    junk = self.is_junk_text(text)
                    text_len = len(text)
                    if junk:
                        text_score = 0.0
                    elif text_len > 200:
                        text_score = 0.7
                    elif text_len > 50:
                        text_score = 0.4  # moderate amount of good text
                    else:
                        text_score = 0.2  # minimal valid text, still better than junk

                    # --- Text density ---
                    text_area = sum(fitz.Rect(b[:4]).get_area() for b in text_blocks if b[4].strip())
                    page_area = bbox.get_area()
                    text_density = text_area / page_area if page_area else 0
                    density_score = min(text_density, 1.0)

                    # --- Image area ---
                    image_area = 0.0
                    image_blocks = [b for b in page.get_text("dict")["blocks"] if b["type"] == 1]  # type 1 = image
                    for img_block in image_blocks:
                        rect = fitz.Rect(img_block["bbox"])
                        img_area = rect.get_area()
                        image_area += img_area

                    image_ratio = image_area / page_area if page_area else 0
                    if image_ratio == 0.0:
                        image_penalty = -0.3  # small reward for image-free pages
                    elif image_ratio < 0.1:
                        image_penalty = 0.0   # neutral
                    else:
                        image_penalty = 0.3   # penalize significant image content

                    # --- Page-level score ---
                    page_score = (0.8 * text_score + 0.1 * density_score) - image_penalty
                    page_score = max(0, min(page_score, 1))
                    page_scores.append(page_score)

            # --- Fallback with pdfplumber if needed and available ---
            if (len(page_scores) == 0 or sum(page_scores) == 0) and PDFPLUMBER_AVAILABLE:
                with pdfplumber.open(self.pdf_options.file_path) as pdf:
                    for page in pdf.pages:
                        fallback_text = page.extract_text()
                        if fallback_text and len(fallback_text.strip()) > 200 and not self.is_junk_text(fallback_text):
                            page_scores.append(1.0)
                        else:
                            page_scores.append(0.0)

            # --- Final decision ---
            avg_score = sum(page_scores) / len(page_scores) if page_scores else 0
            return self.PdfType.DIGITAL if avg_score >= 0.5 else self.PdfType.SCANNED

        except Exception as e:
            raise RuntimeError(f"Error processing PDF: {e}")

def batch_main():
    folder_path = r"C:\Users\sadiqah.mushtaq\OneDrive - Astera Software\Astera\OCR\Digital_Pdfs"
    if not os.path.exists(folder_path):
        print(f"[!] Folder not found: {folder_path}")
        return

    print(f"Processing PDFs in folder: {folder_path}\n")
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            full_path = os.path.join(folder_path, filename)
            try:
                options = CheckPdfTypeOptions(full_path)
                processor = CheckPdfTypeProcessor(options)
                result = processor.process()
                if result == "Scanned":
                    print(f"{filename}: {result}")
            except Exception as e:
                print(f"{filename}: ERROR - {str(e)}")
    print("\nBatch processing complete.")

def main():
    parser = argparse.ArgumentParser(description='Check PDF Type')
    parser.add_argument('-file_path', required=True, help='Path to the PDF file')
    args = parser.parse_args()

    try:
        options = CheckPdfTypeOptions(args.file_path)
        processor = CheckPdfTypeProcessor(options)
        result = processor.process()
        warnings.warn(f"PDF_TYPE_RESULT:{result}")
        warnings.warn("Execution completed")
    except Exception as e:
        warnings.warn(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    # batch_main()
    main()







