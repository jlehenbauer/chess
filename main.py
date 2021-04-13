from chess import Board

def main():
    c = Board()

    c.set_standard()

    while True:
        print(c)
        if c.TURN:
            print("White, it's your turn.")
        else:
            print("Black, it's your turn.")
        
        command = input("Enter your move: ")

        if command == 'exit':
            return 0

        elif command == 'log':
            print(c.log())

        elif command == '':
            pass

        else:
            c.parse(command, True)



if __name__ == "__main__":
    main()