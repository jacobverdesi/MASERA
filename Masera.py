import threading



def Agent(num):
    print("Agent #",num)
    return


def main():
    agents=[]
    for i in range(5):
        t = threading.Thread(target=Agent(i))
        agents.append(t)
        t.start()

if __name__ == '__main__':
    main()