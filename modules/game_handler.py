import time
from threading import Thread
import asyncio
from logging import Logger
from modules.database import db_get_ended_games, db_get_game_data, db_remove_game
from modules.game_starter import start


class GameHandler(Thread):
    def __init__(self, logger: Logger):
        super().__init__()
        self.logger = logger

    def run(self) -> None:
        self.logger.info("Запуск обработчика игр")
        while True:
            games = db_get_ended_games()

            for game_id in games:
                asyncio.run(self.handle(game_id))
            time.sleep(5)

    async def handle(self, game_id: str):
        log = self.logger.getChild(game_id)
        log.info("Запуск обработки игры")

        game_data = db_get_game_data(game_id)
        if len(game_data['players']) == 0:
            log.info("В игре не участвовали пользователи. Удаляю игру из базы данных")
            db_remove_game(game_id)
            return

        try:
            start(game_id)
        except Exception as ex:
            log.exception("Произошла ошибка при обработке игры", exc_info=ex)
        else:
            log.info("Обработка игры успешно завершена")
