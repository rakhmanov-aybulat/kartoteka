import logging

from psycopg2.extensions import connection

from card import Card
from exceptions import CantGetCard

logger = logging.getLogger(__name__)


class PostgresCardStorage:
    """Db abstraction layer"""

    def __init__(self, conn: connection) -> None:
        self.conn = conn

    def add_card(self, card: Card) -> None:
        pass

    def remove_card(self, card: Card) -> None:
        pass

    def update_card(self, card: Card) -> None:
        pass

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
        pass

