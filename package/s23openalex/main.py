"""
Main file of this package.
"""
import click
from .works import Works


@click.command(help="OpenAlex Institutions")
@click.argument("doi")
@click.option(
    "-t",
    "--type",
    type=click.Choice(["bibtex", "ris"]),
    default="bibtex",
    help="Output format (bibtex or ris)",
)
def main(doi, type):
    """Convert DOI to BibTeX or RIS format"""

    mywork = Works(doi)
    if type == "bibtex":
        output = mywork.bibtex
    elif type == "ris":
        output = mywork.ris

    click.echo(output)


if __name__ == "__main__":
    main()
