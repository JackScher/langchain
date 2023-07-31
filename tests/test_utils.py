from app.utils import load_pdf, split_text


def test_load_pdf() -> None:
    pdf_text = load_pdf()
    assert len(pdf_text) > 0


def test_split_text() -> None:
    mock_text = "123456789 012345678 901234"
    chunk_size = 9
    chunks = split_text(mock_text)
    assert len(chunks[0]) == chunk_size
