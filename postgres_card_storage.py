import logging

from psycopg2.extensions import connection

from card import Card
from exceptions import CantAddCard, CantUpdateCard, \
    CantGetCard, CantGetCardTuple


logger = logging.getLogger(__name__)


class PostgresCardStorage:
    """Db abstraction layer"""

    def __init__(self, conn: connection) -> None:
        self.conn = conn

    def add_card(self, card: Card) -> None:
        """
        Takes an instance of the Card class with any ID and
        adds it to the database
        """
        try:
            with self.conn as conn:
                with conn.cursor() as cursor:
                    query = ('INSERT INTO cards (title, content, author, '
                             'book_name, book_edition_number, '
                             'year_of_book_publication, quote_page_number) '
                             'VALUES(%s, %s, %s, %s, %s, %s, %s);')
                    data = (card.title, card.content, card.author,
                            card.book_name, card.book_edition_number,
                            card.year_of_book_publication,
                            card.quote_page_number)
                    cursor.execute(query, data)
        except Exception:
            raise CantAddCard

    def remove_card(self, card: Card) -> None:
        pass

    def update_card(self, card: Card) -> None:
        try:
            with self.conn as conn:
                with conn.cursor() as cursor:
                    query = ('UPDATE cards '
                             'SET title = %s, content = %s, author = %s, '
                             'book_name = %s, book_edition_number = %s, '
                             'year_of_book_publication = %s, '
                             'quote_page_number = %s '
                             'WHERE id = %s;')
                    data = (card.title, card.content, card.author,
                            card.book_name, card.book_edition_number,
                            card.year_of_book_publication,
                            card.quote_page_number, card.id)
                    cursor.execute(query, data)
        except Exception:
            raise CantUpdateCard

    def get_card(self, card_id: int) -> Card:
        try:
            with self.conn as conn:
                with conn.cursor() as cursor:
                    query = 'SELECT * FROM cards WHERE id = %s'
                    cursor.execute(query, (card_id,))
                    card = cursor.fetchone()

                    if card is None:
                        raise CantGetCard()

                    return Card(*card)
        except Exception:
            raise CantGetCard

    def get_card_tuple(self) -> tuple[Card, ...]:
        try:
            with self.conn as conn:
                with conn.cursor() as cursor:
                    query = 'SELECT * FROM cards;'
                    cursor.execute(query)
                    card_tuple = cursor.fetchall()
                    card_tuple = tuple([Card(*card) for card in card_tuple])
                    return card_tuple
        except Exception:
            raise CantGetCardTuple

