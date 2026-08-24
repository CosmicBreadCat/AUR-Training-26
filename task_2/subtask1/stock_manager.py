FILENAME = 'stock.txt'
MENU = '''
Welcome to the stock management system:
- Enter 1 to add stock to an item
- Enter 2 to remove stock from an item
- Enter 3 to view current stock
- Enter 4 to exit system 
'''

class StockManager:
    def __init__(self, filename):
        self.filename = filename
        with open(self.filename, 'r') as f:
            lines = [line for line in f.read().split('\n') if line]
            self.__stock = dict(map(lambda x: (x.split(',')[0], int(x.split(',')[1])), lines))

    def save(self):
        with open(self.filename, 'w') as f:
            for name, qty in self.__stock.items():
                f.write(f'{name},{qty}\n')

    def show_stock(self):
        print('\nCurrent stock:')
        for i, (key, value) in enumerate(self.__stock.items(), start=1):
            print(f'{i}. {key}: {value}')

    def resolve_key(self, num):
        try:
            return list(self.__stock)[num]
        except IndexError:
            print(f'Key with index {num} does not exist.')

    def add_stock(self, key, amount):
        try:
            updated = self.__stock.get(key) + amount
            self.__stock[key] = updated
            self.save()
        except KeyError:
            print(f'Key {key} does not exist.')

    def remove_stock(self, key, amount):
        try:
            updated = self.__stock.get(key) - amount
            if updated < 0:
                print('Amount requested for removal less than stock, removal canceled.')
            else:
                self.__stock[key] = updated
                self.save()
        except KeyError:
            print(f'Key {key} does not exist.')

def main():
    manager = StockManager(FILENAME)
    flag = False

    while not flag:
        print(MENU)
        while True:
            choice = input('Enter your choice: ').strip()
            try:
                value = int(choice)
                match value:
                    case 1:
                        choice = input('Enter your choice of item (type "back" to exit): ').strip().lower()
                        key = choice
                        if choice.isdigit():
                            key = manager.resolve_key(int(choice)-1)
                        elif choice == 'back':
                            continue

                        amount = input('Enter amount to add: ').strip()
                        if not (amount.isdigit() and int(amount) > 0):
                            print('Input must be a positive integer.')
                            continue

                        manager.add_stock(key, int(amount))
                        break
                    case 2:
                        choice = input('Enter your choice of item (type "back" to exit): ').strip().lower()
                        key = choice
                        if choice.isdigit():
                            key = manager.resolve_key(int(choice) - 1)
                        elif choice == 'back':
                            continue

                        amount = input('Enter amount to add: ').strip()
                        if not (amount.isdigit() and int(amount) > 0):
                            print('Input must be a positive integer.')
                            continue

                        manager.remove_stock(key, int(amount))
                        break
                    case 3:
                        manager.show_stock()
                        break
                    case 4:
                        flag = True
                        print('Exiting program.')
                        break
                    case _:
                        print('Invalid choice.')
                        continue
            except ValueError:
                continue

if __name__ == '__main__':
    main()