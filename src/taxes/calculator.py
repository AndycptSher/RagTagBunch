def calculation(country):
    with open(country+".txt", "r")as tax1:
        tax = tax1.readlines()
    for x, y in enumerate(tax):
        tax[x] = y[:len(y) - 1]

    income = int(input("how much do you make per month?: "))

    income -= int(input("How much is used in business?"))

    i = 0
    taxed_amount = 0
    while income > 0:
        if len(tax[i].split(",")) == 1 or int(tax[i].split(",")[1]) > income:
            taxed_amount += income * int(tax[i].split(",")[0]) / 100
            break
        elif int(tax[i].split(",")[1]) < income or len(tax[i].split(",")) == 2:
            taxed_amount += int(tax[i].split(",")[1]) * int(tax[i].split(",")[0]) / 100
            income -= int(tax[i].split(",")[1])
        i += 1
    print(taxed_amount)
