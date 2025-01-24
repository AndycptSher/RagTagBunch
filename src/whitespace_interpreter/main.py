# https://www.codewars.com/kata/reviews/55d7da1ba7692a4d7f00002a/groups/63adb861a68bfa00019aa773

# to help with debugging
def unbleach(n):
    return n.replace(' ', 's').replace('\t', 't').replace('\n', 'n')

class decisionTrie:
    def __init__(self):
        self.choices = {}
    
    def set(self, option, *payload):
        if len(option) == 1:
            self.choices[option] = tuple([*payload])
            return self
        self.choices[option[0]] = self.choices.get(option[0], decisionTrie()).set(option[1:], *payload)

        return self
    
    def fill(self, feed):
        # print("feed", unbleach(feed))
        if not feed:
            raise Exception("Something's wrong, I can feel it.")# if it stops abbruptly aka not valid input/code
        match = self.choices[feed[:1]]
        # terminal
        if type(match) == tuple:
            # if is sole command
            if len(match) == 1:
                return feed[1:], match[0]
        # if a number or label is trailing
            feed , content = match[1](feed[1:])
            return feed, (lambda :match[0][0](content), match[0][1].format(content if type(content) == int else unbleach(content)))
            
        return match.fill(feed[1:])
    
    def __str__(self):
        return "\n".join([f"{x}: {str(self.choices[x])}" for x in self.choices])+"\n"
    

def extNum(feed):
    cut = feed.index("\n")
    if cut == 0: raise Exception("Invalid expression")

    elif cut == 1:
        return feed[2:], 0

    sign = {"\t": -1, " ": 1}[feed[0]]
    number = [*feed[1:cut].replace("\t", "1").replace(" ", "0")]
    twosComp = [2**x for x in range(len(number)-1,-1,-1)]
    t = sign*sum(map(lambda a: int(a[0])*a[1], zip(number, twosComp)))
    return feed[cut+1:], t

def extLabel(feed):
    cut = feed.index("\n")
    if cut == -1: raise Exception("404:Terminal not Found")
    return feed[cut+1:], unbleach(feed[:cut+1])

# solution
def whitespace(code, inp = ''):
    
    # could have used a class, to lazy to refactor
    global acc, labels # variables that are involved in assignment
    inpu = inp.strip().split("\n") if inp.strip().count("\n")>=1 else [*inp]
    output = []
    stack = []    
    heap = {}
    acc = 0
    labels = {}
    callStack= []
    def getCheck(stack, index):
        if type(index) != int: raise Exception()
        if 0 > index: raise Exception()
        if index >= len(stack): raise Exception()
        return index
    
    def slideCheck(stack, slide):
        if type(slide) != int:raise Exception()
        if 0 > slide or slide >= len(stack):
            return len(stack)-1
        return slide
    
    def divCheck(num):
        if not num: raise Excpetion("divide by 0")
        return num
        
    def accSet(label):
        global acc, labels
        if type(label) == str:
            acc = labels[label]
        else:
            acc = label

    
    dec = decisionTrie()
    #push num to stack
    dec.set("  ", (lambda a: stack.append(a), "push {} onto stack"), extNum)
    #dup top of stack
    dec.set(" \n ", (lambda: stack.append(stack[-1]), "duplicate top of stack"))
    #copy nth number in the stack
    dec.set(" \t ", (lambda a: stack.append(stack[getCheck(stack, len(stack)-a-1)]), "copy {}th number in stack"), extNum)
    #swap top two in stack
    dec.set(" \n\t", (lambda: stack.append(stack.pop(-2)), "swap top two in stack"))
    #pop stack
    dec.set(" \n\n", (lambda: stack.pop(), "pop stack"))
    #slide n items off the stack, keeping top item
    dec.set(" \t\n", (lambda a: [stack.pop(-2) for x in range(slideCheck(stack,a))], "sliding {} numbers off the stack, keeping the top"), extNum)
    #heap set
    dec.set("\t\t ", (lambda:heap.__setitem__(stack.pop(-2), stack.pop()), "sets top of stack at value \'stack second top\'"))
    #heap access
    dec.set("\t\t\t", (lambda: stack.append(heap[stack.pop()]), "access heap address \'stack top\' and push to stack"))
    #add
    dec.set("\t   ", (lambda: stack.append(stack.pop()+stack.pop()), "push sum of top two of stack"))
    #sub
    dec.set("\t  \t", (lambda: stack.append(stack.pop(-2)-stack.pop()), "push difference of top two in stack"))
    #mul
    dec.set("\t  \n", (lambda: stack.append(stack.pop()*stack.pop()), "push product of top two in stack"))
    #div
    dec.set("\t \t ", (lambda: stack.append(stack.pop(-2)//divCheck(stack.pop())), "push quotent of top two in stack"))
    #mod
    dec.set("\t \t\t", (lambda: stack.append(stack.pop(-2)%divCheck(stack.pop())), "push quotent of top two in stack"))
    #output as int
    dec.set("\t\n \t", (lambda: output.append(str(stack.pop())), "output top as int"))
    #output as chr
    dec.set("\t\n  ", (lambda: output.append(chr(stack.pop())), "output Top as chr"))
    #set char from input into heap at top of stack
    dec.set("\t\n\t ", (lambda: heap.__setitem__(stack.pop(), ord(inpu.pop(0))), "set char from input into heap at \'top of stack\'"))
    #set int from input into heap at top of stack
    dec.set("\t\n\t\t", (lambda: heap.__setitem__(stack.pop(), inpu.pop(0)), "set num from input into heap at \'top of stack\'"))
    #mark label
    dec.set("\n  ", (lambda a:"hello", "label {}"), extLabel)# <-comment crucial, funcion redudant(well well well, how the turntables)
    #call subroutine
    dec.set("\n \t", (lambda a:[x for x in [callStack.append(acc), accSet(a)]], "call subroutine with {}"), extLabel)
    #jump to label
    dec.set("\n \n", (lambda a:accSet(a), "jump to {}"), extLabel)
    #jump if stack top is 0
    dec.set("\n\t ", (lambda a:accSet(a) if stack.pop() ==0 else 0, "jump to {} if top of stack is 0"), extLabel)
    #jump if stack top is less than 0
    dec.set("\n\t\t", (lambda a:accSet(a) if stack.pop() < 0 else 0, "jump to {} if top of stack is less than 0"), extLabel)
    #exit subroutine
    dec.set("\n\t\n", (lambda: accSet(callStack.pop()), "exit subroutine"))
    #terminal
    dec.set("\n\n\n", (lambda: 58008, "terminate"))
    #print(dec)
    print("Done initalizing\n")
    
    #...
    #filter out the non-essentials
    cleaned = "".join([x for x in code if x in (" ","\t", "\n")])
    
    cleaned, steps = dec.fill(cleaned)
    steps = [steps]
    while cleaned:
        cleaned, operators = dec.fill(cleaned)
        steps.append(operators)
        
    if inpu: print("input", inpu)
    
    print("\'assembly\' code")
    for index, x in enumerate(steps):
        if x[1].startswith("label "):
            if labels.get(x[1][6:], None) is not None: raise Exception("repeat label")
            labels[x[1][6:]] = index
        print("\t"+x[1])
        
    if labels:
        print("labels", labels)
        print("done interpreting labels")
    
    while acc >= 0:
        print()
        print(acc,": ", steps[acc][1], sep="")
        if steps[acc][1] == "terminate":
            break
        if inpu: print("input", inpu)
        steps[acc][0]()
        print("stack", stack)
        print("heap", heap)
        if labels: print("callStack", callStack)
        acc += 1
    
    print("output", "".join(output))
    return "".join(output)
