"""
The work class.
"""
#!/usr/bin/env python
import base64
import requests
import bibtexparser
from IPython.display import display, HTML


class Works:
    """A work class."""

    def __init__(self, oaid):
        self.oaid = oaid
        self.req = requests.get(
            f"https://api.openalex.org/works/{oaid}"
        )  # get the requests
        self.data = self.req.json()  # convert to json data

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        _authors = [
            au["author"]["display_name"] for au in self.data["authorships"]
        ]  # get authors in authorships

        # deal with different number of authors
        if len(_authors) == 1:
            authors = _authors[0] + ", "
        elif len(_authors) == 0:
            authors = ""
        else:
            authors = ", ".join(_authors[0:-1]) + " and " + _authors[-1] + ", "

        # get title
        title = self.data["title"]

        # get biblio information, deal with different situations
        # deal with volume
        if self.data["biblio"]["volume"] is None:
            volume = ""
        else:
            volume = self.data["biblio"]["volume"] + ", "
        # deal with issue
        issue = self.data["biblio"]["issue"]
        if issue is None:
            issue = ""
        else:
            issue = issue + ", "
        # deal with pages
        if (
            self.data["biblio"]["first_page"] is None
            and self.data["biblio"]["last_page"] is None
        ):
            pages = ""
        elif (
            self.data["biblio"]["first_page"] is None
            and self.data["biblio"]["last_page"] is not None
        ):
            pages = self.data["biblio"]["last_page"] + ", "
        elif (
            self.data["biblio"]["last_page"] is None
            and self.data["biblio"]["first_page"] is not None
        ):
            pages = self.data["biblio"]["first_page"] + ", "
        else:
            pages = (
                "-".join(
                    [
                        self.data["biblio"]["first_page"],
                        self.data["biblio"]["last_page"],
                    ]
                )
                + ", "
            )

        # get publication year
        year = self.data["publication_year"]

        # get citation count
        citedby = self.data["cited_by_count"]

        # get id
        oa_id = self.data["id"]

        # combine all information and form a string
        string = (
            f"{authors}{title}, {volume}{issue}{pages}({year}), "
            f'{self.data["doi"]}. cited by: {citedby}. {oa_id}'
        )

        return string

    # get a bibtex entry of this work
    @property  # decorator
    def bibtex(self):
        """Bibtex generating function."""

        bib_dict = {}

        # get authors in authorships
        _authors = [au["author"]["display_name"] for au in self.data["authorships"]]

        # deal with different number of authors
        if len(_authors) == 1:
            authors = _authors[0] + ", "
        elif len(_authors) == 0:
            authors = ""
        else:
            authors = ", ".join(_authors[0:-1]) + " and " + _authors[-1] + ", "

        # get last name of the author
        last_name = _authors[0].split()[-1].lower()

        # get title
        bib_dict["title"] = self.data["title"]

        # get the representative word
        rep_word = bib_dict["title"].split()[0].lower()

        # get doi and url
        url = self.data["doi"]
        parts = url.rsplit("/", 2)
        doi = parts[1] + "/" + parts[2]

        # get journal
        bib_dict["journal"] = self.data["host_venue"]["display_name"]

        # get biblio information, deal with different situations
        # deal with volume
        if self.data["biblio"]["volume"] is not None:
            bib_dict["volume"] = self.data["biblio"]["volume"]

        # deal with number
        bib_dict["number"] = self.data["biblio"]["issue"]
        if bib_dict["number"] is None:
            bib_dict["number"] = ""

        # deal with pages
        if (
            self.data["biblio"]["first_page"] is None
            and self.data["biblio"]["last_page"] is None
        ):
            pages = ""
        elif (
            self.data["biblio"]["first_page"] is None
            and self.data["biblio"]["last_page"] is not None
        ):
            pages = self.data["biblio"]["last_page"]
        elif (
            self.data["biblio"]["last_page"] is None
            and self.data["biblio"]["first_page"] is not None
        ):
            pages = self.data["biblio"]["first_page"]
        else:
            pages = "-".join(
                [self.data["biblio"]["first_page"], self.data["biblio"]["last_page"]]
            )

        # get publication year
        year = self.data["publication_year"]

        # format the bib dictionary
        bib_dict["ENTRYTYPE"] = "article"
        bib_dict["ID"] = f"{last_name}-{year}-{rep_word}"
        bib_dict["authors"] = authors
        bib_dict["doi"] = doi
        bib_dict["pages"] = pages
        bib_dict["url"] = url
        bib_dict["year"] = f"{year}"

        bib_database = bibtexparser.bibdatabase.BibDatabase()
        bib_database.entries = [bib_dict]

        # use bibtexparser to parse the dict
        formatted_bib = bibtexparser.dumps(bib_database)

        # present on jupyter notebook website
        bib64 = base64.b64encode(formatted_bib.encode("utf-8")).decode("utf8")
        uri = f'<pre>{formatted_bib}<pre><br><a href="data:text/plain;base64,\
                {bib64}" download="bibtex">Download bibtex</a>'

        display(HTML(uri))
        return formatted_bib

    @property
    def ris(self):
        """Ris generating function."""
        fields = []
        if self.data["type"] == "journal-article":
            fields += ["TY  - JOUR"]
        else:
            raise Exception("Unsupported type {self.data['type']}")

        for author in self.data["authorships"]:
            fields += [f'AU  - {author["author"]["display_name"]}']

        fields += [f'PY  - {self.data["publication_year"]}']
        fields += [f'TI  - {self.data["title"]}']
        fields += [f'JO  - {self.data["host_venue"]["display_name"]}']
        fields += [f'VL  - {self.data["biblio"]["volume"]}']

        if self.data["biblio"]["issue"]:
            fields += [f'IS  - {self.data["biblio"]["issue"]}']

        fields += [f'SP  - {self.data["biblio"]["first_page"]}']
        fields += [f'EP  - {self.data["biblio"]["last_page"]}']
        fields += [f'DO  - {self.data["doi"]}']
        fields += ["ER  -"]

        ris = "\n".join(fields)
        ris64 = base64.b64encode(ris.encode("utf-8")).decode("utf8")
        uri = f'<pre>{ris}<pre><br><a href="data:text/plain;base64,\
                {ris64}" download="ris">Download RIS</a>'

        display(HTML(uri))
        return ris
