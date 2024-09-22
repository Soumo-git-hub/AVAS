import multiprocessing

# To run AVAS
def startAvas():
    print("Process 1 is running.")
    from main import start
    start()

# To run hotword
def listenHotword():
    print("Process 2 is running.")
    from engine.features import hotword
    hotword()

# Start both processes
if __name__ == '__main__':
    try:
        p1 = multiprocessing.Process(target=startAvas)
        p2 = multiprocessing.Process(target=listenHotword)

        p1.start()
        p2.start()

        p1.join()

        if p2.is_alive():
            p2.terminate()
            p2.join()

        print("System stopped.")

    except KeyboardInterrupt:
        print("Manual interrupt received. Terminating processes...")
        p1.terminate()
        p2.terminate()

        p1.join()
        p2.join()

        print("Processes terminated and system stopped.")
