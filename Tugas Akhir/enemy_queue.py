class QueueNode:
    def __init__(self, enemy):
        self.enemy = enemy
        self.next = None

class EnemyQueue:
    def __init__(self):
        self.front = None
        self.rear = None

    def enqueue(self, enemy):
        new_node = QueueNode(enemy)

        # empty queue
        if self.rear is None:
            self.front = new_node
            self.rear = new_node

            return

        self.rear.next = new_node
        self.rear = new_node

    def dequeue(self):
        if self.front is None:
            return None

        removed_enemy = self.front.enemy
        self.front = self.front.next

        # queue becomes empty
        if self.front is None:
            self.rear = None

        return removed_enemy

    def is_empty(self):
        return self.front is None