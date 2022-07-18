import scheduler


def main():
    schedulers = scheduler.get_scheduler()
    while True:
        print("Select Schedular(or q to quit)")
        for i in range(len(schedulers)):
            print(f"{i}:{schedulers[i][0]}")
        i = input()
        if (i == "q"):
            break
        if (not (i in map(str, range(len(schedulers))))):
            print("Invalided Input")
            continue

        schedulers[int(i)][1]().start()


if __name__ == '__main__':
    main()
