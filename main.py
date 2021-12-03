from interface.console_interface import TapAI

if __name__ == '__main__':
    game = TapAI('naive_embeddings')
    game.printBoard()
    while True:
        game.playerATurn()
