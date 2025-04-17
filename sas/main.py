from sas.models import Word, Pool


class Server:
    """Main class."""

    def __init__(self):
        """Init method"""
        self.db = DB()

    def get_word(self) -> Word:
        """Start the program."""
        raise NotImplementedError


class Runner:
    pool: Pool | None = None

    def __init__(self, server: Server):
        self.server = server

    def run(self):
        while True:
            pool = server.get_pool()
            while True:
                word = pool.get_word()
                print(word.translate)
                answer = input("(Press Ctl-C for exit) > ")
                server.check(word, answer)
        raise NotImplementedError


def main():
    # import sys
    # _old_excepthook = sys.excepthook
    #
    # def myexcepthook(exctype, value, traceback):
    #     if exctype == KeyboardInterrupt:
    #         print
    #         "Handler code goes here"
    #     else:
    #         _old_excepthook(exctype, value, traceback)
    #
    # sys.excepthook = myexcepthook



    # try:
    #     main()
    # except KeyboardInterrupt:
    #     ...
    #
    # def main():
    #     ...


    server = Server()
    runner = Runner(server)
    runner.run()
