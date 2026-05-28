# fungsi rotasi turn menggunakan circular linked list
class TurnNode:
    def __init__(self, name):
        self.name = name
        self.next = None

class TurnRotation:
    def __init__(self):
        self.head = None
        self.current = None

    def add_turn(self, name):
        new_node = TurnNode(name)

        # first node
        if self.head is None:
            self.head = new_node
            new_node.next = self.head

            return

        temp = self.head
        while temp.next != self.head:
            temp = temp.next
        temp.next = new_node
        new_node.next = self.head

    def start(self):
        self.current = self.head

    def next_turn(self):
        turn = self.current.name
        self.current = self.current.next
        return turn
    
    def set_player_turn(self):
        self.current = self.head