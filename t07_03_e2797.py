import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    size = 1 << 18
    mask = size - 1
    table = [0] * size
    count = 0
    for k in range(1, n + 1):
        x = int(data[k])
        i = (x * 2654435761) & mask
        while True:
            v = table[i]
            if v == 0:
                table[i] = x
                count += 1
                break
            if v == x:
                break
            i = (i + 1) & mask
    print(count)


main()
