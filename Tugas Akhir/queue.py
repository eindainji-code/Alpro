class Queue:
    def __init__(self):
        self.data = []

    # Menambahkan data ke belakang queue
    def enqueue(self, item):
        self.data.append(item)

    # Menghapus data paling depan queue
    def dequeue(self):
        if self.is_empty():
            return None
        return self.data.pop(0)

    # Melihat data paling depan
    def front(self):
        if self.is_empty():
            return None
        return self.data[0]

    # Mengecek queue kosong atau tidak
    def is_empty(self):
        return len(self.data) == 0

    # Menampilkan isi queue
    def display(self):
        return self.data

# SIMULASI MUSUH DATANG

enemy_queue = Queue()

# Menambahkan musuh ke queue
enemy_queue.enqueue("Zombie")
enemy_queue.enqueue("Slime")
enemy_queue.enqueue("Wolf")

print("Queue Musuh:")
print(enemy_queue.display())

print("\n=== Battle Start ===")

# Selama queue masih ada isinya
while not enemy_queue.is_empty():

    # Musuh paling depan dilawan dulu
    enemy = enemy_queue.dequeue()

    print(f"\nMusuh yang dilawan: {enemy}")
    print(f"{enemy} berhasil dikalahkan!")

    # Menampilkan sisa musuh
    print("Sisa queue musuh:", enemy_queue.display())

print("\nSemua musuh berhasil dikalahkan!")