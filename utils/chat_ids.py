def read_chat_ids():
    chat_ids = []
    with open('chat_ids.txt', 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                chat_ids.append(int(line))
    return chat_ids

def add_chat_id(chat_id):
    with open('chat_ids.txt', 'a') as file:
        file.write(str(chat_id) + '\n')