import socket


def send_number():
    while True:
        # Prompt user for input
        user_input = input("Enter a number (or 'q' to quit): ")

        # Check if the user wants to quit
        if user_input.lower() == 'q':
            print("Exiting client...")
            break

        try:
            # Convert the input to a float
            number_a = float(user_input)

            # Establish a connection to the server
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(('localhost', 9999))

            # Send the number A
            client.send(str(number_a).encode('utf-8'))

            # Receive the sequence from the server
            response = client.recv(1024).decode('utf-8')
            sequence = list(map(float, response.split(',')))
            print("\nGolden ratio sequence:")
            for idx, num in enumerate(sequence, 1):
                print(f"{idx}: {num}")
            print("\n")
        except ValueError:
            print("Please enter a valid number.")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            client.close()


if __name__ == "__main__":
    send_number()