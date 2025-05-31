class Printer:
    def process(self, board):
        """Simulate stencil paste printing."""
        board.status = "PRINTED"
        return board
