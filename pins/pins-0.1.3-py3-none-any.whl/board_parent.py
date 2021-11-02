class Board:
    """
    main board class
    """

    def __init__(self, board_type):
        self.board_type = board_type


    def pin_meta(self):
        """
        Read metadata from pin
        """

    def info(self):
        """
        display the status of the board
        """
        print("Board info:")
        # print("* Name: {}".format(self.name))
        print("* Type: {}".format(self.board_type))
