import time
# Single Linked List Untuk Sistem Inventory
class itemNode: 
    def __init__(self,item):
        self.item = item
        self.next = None

class Inventory:
    def __init__(self):
        self.head = None

    def add_item(self,item, show_message = True):
        new_node = itemNode(item)

        if self.head is None:
            self.head = new_node # jika belum ada item, head menjadi item pertama

        else:
            current = self.head

            while current.next:
                current = current.next
            current.next = new_node

        if show_message:
            print(f"{item} collected!")
            time.sleep(0.5)

    def show_inventory(self):
        if self.head is None:

            print("\nInventory is empty!")
            time.sleep(0.2)
            return
        
        print("\nINVENTORY")
        current = self.head

        number = 1

        while current:
            print(f"{number}. {current.item}")

            current = current.next 

            number += 1

    def search_item(self,target):
        current = self.head

        while current:
            if current.item.lower() == target.lower():

                print(f"\n{target} found!")
                return current.item
            
            current = current.next

        print(f"\n{target} not found!")
        return None
    
    # hapus item
    def remove_item(self, target):

        # inventory kosong
        if self.head is None:

            print("\nInventory empty!")
            return

        if self.head.item.lower() == target.lower():

            self.head = self.head.next

            print(f"\n{target} removed!")
            return

        # cari item
        current = self.head

        while current.next:

            if current.next.item.lower() == target.lower():

                current.next = current.next.next

                print(f"\n{target} removed!")
                return

            current = current.next

        print(f"\n{target} not found!")

    def to_list(self):

        items = []

        current = self.head

        while current:

            items.append(current.item)

            current = current.next

        return items
