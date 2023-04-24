"""
Main file of this package.
"""
import click
from .works import Works


@click.command(help="OpenAlex Institutions")
@click.argument("doi")
@click.option(
    "-b",
    "--bibtex",
    is_flag=True,
    help="Output in BibTeX format",
)
@click.option(
    "-r",
    "--ris",
    is_flag=True,
    help="Output in RIS format",
)
def main(doi, bibtex, ris):
    """Convert DOI to BibTeX or RIS format"""

    if bibtex:
        mywork = Works(doi)
        output = mywork.bibtex
    elif ris:
        mywork = Works(doi)
        output = mywork.ris
    else:
        click.echo("Please specify an output format (-b/--bibtex or -r/--ris)")

    click.echo(output)
