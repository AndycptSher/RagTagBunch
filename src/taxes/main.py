import calculator, glob

#calculator.calculation("1tax")
entry = input("Press Enter to Start: ")
if entry == "add":
    with open(input("What place?")+".txt", "a")as new:
        i = 1
        adder = ""
        while adder.split(",") != 1:
            print("loop", i)
            while True:
                try:
                    thing = int(input(f"bracket {i} percentage"))
                    break
                except ValueError:
                    print("input a number")
            adder = str(thing)
            thing = "A"
            while thing != "":
                try:
                    thing = ","+str(int(input("input amount")))
                    break
                except Exception as error:
                    print("highest bracket achieved")
                    thing = ""
            adder += thing+"\n"
            new.write(str(adder))
            i += 1
            if thing == "":
                break
elif entry == "":
    places = []
    for x in glob.glob("*.txt"):
        places.append(x[:len(x)-4])
    while True:
        try:
            country = input("which tax code? ex. "+", ".join(places))
            calculator.calculation(country)
        except FileNotFoundError:
            if country == "":
                break
            print("Please try again, if this occurs again, please enter the brackets yourself")
