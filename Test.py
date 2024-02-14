list = []
def get_chetn(n):
    for i in range(n):
        if i % 2 == 0:
            print(i)
            list.append(i)


s = int(input())
get_chetn(s)
print(*list)

