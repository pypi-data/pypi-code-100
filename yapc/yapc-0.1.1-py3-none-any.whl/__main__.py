from pathlib import Path
from typing import List, Tuple

import click
from PyPDF2 import PdfFileReader
from PyPDF2.pdf import PdfFileWriter

from yapc.param import PageNoList, PDFReader


@click.group()
def cli():
    pass


@cli.command()
@click.argument("pdf", type=PDFReader())
def inspect(pdf: PdfFileReader):
    info = pdf.getDocumentInfo()
    page_count = pdf.getNumPages()
    is_encrypted = pdf.getIsEncrypted()

    click.echo(f"Page Count: {page_count}")
    click.echo(f"Is Encrypted: {is_encrypted}")
    for key, value in dict(info).items():
        if not value:
            continue
        name = key.strip("/")
        value = value.strip("/")
        click.echo(f"{name}: {value}")


@cli.command(help="Extract pages from a PDF file")
@click.argument("pdf", type=PDFReader())
@click.argument("pages", nargs=-1, type=PageNoList())
@click.option(
    "--out",
    "-o",
    required=True,
    help="Name of the output file",
    type=click.Path(
        file_okay=True,
        dir_okay=False,
        writable=True,
        resolve_path=True,
        path_type=Path,
    ),
)
@click.option(
    "--force",
    "-f",
    is_flag=True,
    default=False,
    help="Overwrite output file if it exists",
)
def extract(pdf: PdfFileReader, pages: List[List[str]], out: Path, force: bool):
    pages = [page for page_list in pages for page in page_list]

    writer = PdfFileWriter()
    for page in pages:
        writer.addPage(pdf.getPage(page))
    if (
        not out.exists()
        or force
        or click.confirm(f"File '{out}' already exists. Overwrite?")
    ):
        with open(out, "wb") as out_pdf:
            writer.write(out_pdf)


@cli.command(help="Merge multiple PDF files")
@click.option(
    "--in",
    "-i",
    "pdfs",
    required=True,
    multiple=True,
    help="Input PDF with option page numbers, and ranges",
    type=(PDFReader(), PageNoList(allow_all=True)),
)
@click.option(
    "--out",
    "-o",
    required=True,
    help="Name of the output file",
    type=click.Path(
        file_okay=True,
        dir_okay=False,
        writable=True,
        resolve_path=True,
        path_type=Path,
    ),
)
@click.option(
    "--force",
    "-f",
    is_flag=True,
    default=False,
    help="Overwrite output file if it exists",
)
def merge(pdfs: List[Tuple[PdfFileReader, List[int]]], out: Path, force: bool):
    writer = PdfFileWriter()
    for reader, pages in pdfs:
        pages = pages if pages else list(range(reader.getNumPages()))
        for page in pages:
            writer.addPage(reader.getPage(page))

    if (
        not out.exists()
        or force
        or click.confirm(f"File '{out}' already exists. Overwrite?")
    ):
        with open(out, "wb") as out_pdf:
            writer.write(out_pdf)


cli()
