from typing import NamedTuple


class Card(NamedTuple):
    id: int
    title: str
    content: str
    author: str
    book_name: str
    book_edition_number: int | None
    year_of_book_publication: int | None
    quote_page_number: int | None

