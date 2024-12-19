import time


def alert(x1, y2):
    for _ in range(x1):
        for _ in range(y2):
            print("\a")


with open("schedule.txt", "r")as schedule:
    schedules = schedule.readlines()
printed = ""
while True:
    time.sleep(1)
    current_time = time.ctime()
    minuit = int(current_time[11:13]) * 60 + int(current_time[14:16])
    for x in schedules:
        y = x.split("_")[0]
        if "S" in current_time and printed != "It's the weekend!":
            printed = "It's the weekend!"
            alert(2, 2)
            print(printed)
        elif "S" in current_time:
            pass
        elif int(y.split("-")[0].split(":")[0]) * 60 + int(y.split("-")[0].split(":")[1]) < minuit < int(y.split("-")[1].split(":")[0]) * 60 + int(y.split("-")[1].split(":")[1]) and \
                printed != x.split("_")[1]:  # check if in time range
            printed = x.split("_")[1]
            alert(2, 2)
            print(printed)
