import xmlrpc.client
import datetime

def menu():
    print("1) Add note")
    print("2) Get note")
    print("3) Wikipedia: ")
    print("4) Quit")

def main():
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000", allow_none=True)
    while True:
        menu()
        choice = input("Enter your option: ").strip()
        if choice == "1":
            topic = input("Enter topic: ").strip()
            notename = input("Enter note name: ").strip()
            text = input("Enter text: ").strip()
            timestamp = datetime.datetime.now().isoformat()
            try:
                result = proxy.add_note(topic, notename, text, timestamp)
                if result:
                    print("Note added successfully.")
                else:
                    print("Failed to add note.")
            except Exception as e:
                print(f"Error adding note: {e}")
        elif choice == "2":
            topic = input("Enter topic: ").strip()
            try:
                notes = proxy.get_notes(topic)
                if notes:
                    print(f"Notes for topic '{topic}':")
                    for note in notes:
                        print(f"Note Name: {note.get('notename', '')}")
                        print(f"[{note['timestamp']}] {note['text']}")
                else:
                    print(f"No notes found for topic '{topic}'.")
            except Exception as e:
                print(f"Error getting notes: {e}")
        elif choice == "3":
            topic = input("Enter topic for Wikipedia lookup: ").strip()
            try:
                print(f"Wikipedia info added: {proxy.query_wiki(topic)}")
            except Exception as e:
                print(f"Error")
        elif choice == "4":
            print("Exiting client.")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
