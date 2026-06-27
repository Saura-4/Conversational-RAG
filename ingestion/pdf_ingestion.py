from collections import defaultdict
from unstructured.partition.pdf import partition_pdf


def read_pdf_pages(file_path: str):
    """
    Read a PDF while preserving page boundaries.

    Returns:
        [
            {
                "page": 1,
                "text": "..."
            },
            ...
        ]
    """

    elements = partition_pdf(file_path)

    pages = defaultdict(list)

    for element in elements:

        text = str(element).strip()

        if not text:
            continue

        page = getattr(element.metadata, "page_number", 1)

        pages[page].append(text)

    return [
        {
            "page": page,
            "text": "\n".join(texts)
        }
        for page, texts in sorted(pages.items())
    ]