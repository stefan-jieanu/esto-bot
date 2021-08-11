from pathlib import Path


def main():
    lines = 0;

    for path in Path('server').rglob('*.py'):
        lines += len(open(path).readlines())

    for path in Path('client').rglob('*.py'):
        lines += len(open(path).readlines())

    print("Wow! Your program is " + str(lines) + " lines of code! °˖✧◝(⁰▿⁰)◜✧˖° ") 

main()