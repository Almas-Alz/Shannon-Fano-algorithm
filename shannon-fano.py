import collections
from math import log2


class Char:
    def __init__(self, name, probability):
        self.name = name
        self.probability = probability
        self.code = ''

    def __lt__(self, other):
        return True if self.probability < other.get_probability() else False

    def __str__(self):
        return '{0}\t{1:.2f}\t{2}'.format(self.name, self.probability, self.code)

    def get_name(self):
        return self.name

    def get_probability(self):
        return self.probability

    def get_code(self):
        return self.code

    def append_code(self, code):
        self.code += str(code)


def p_sort(lst):
    for i in range(len(lst)):
        for j in range(0, len(lst) - 1):
            if lst[j].__lt__(lst[j + 1]):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
    return lst


def find_middle(lst):
    if len(lst) == 1:
        return None

    optimal_diff = 0
    mid = 0

    for i in range(len(lst)):
        optimal_diff += lst[i].get_probability()

    for i in range(len(lst)):
        s1 = 0
        s2 = 0
        for j in range(0, len(lst[:i])):
            s1 += lst[j].get_probability()
        for j in range(i, len(lst)):
            s2 += lst[j].get_probability()

        curr_diff = abs(s1 - s2)

        if curr_diff < optimal_diff:
            optimal_diff = curr_diff
            mid = i
    return mid - 1


def shannon_fano(lst):
    mid = find_middle(lst)
    if mid is None: return
    for i in lst[:mid+1]:
        i.append_code(0)
    shannon_fano(lst[:mid+1])
    for i in lst[mid+1:]:
        i.append_code(1)
    shannon_fano(lst[mid+1:])


def main():
    word = str(input())
    ln_word = len(word)
    lst = []
    for k, v in collections.Counter(word).items():
        p = ((v * 100) / ln_word) / 100
        lst.append(Char(k, p))

    sorted_lst = p_sort(lst)
    shannon_fano(sorted_lst)

    print('x\tp\t\tcode')
    for i in range(len(sorted_lst)):
        print(sorted_lst[i])

    h_x = 0
    ml = 0
    for i in range(len(sorted_lst)):
        h_x += sorted_lst[i].get_probability() * log2(sorted_lst[i].get_probability())
        ml += sorted_lst[i].get_probability() * len(sorted_lst[i].get_code())
    h_x = -h_x

    print('\nH(x) = {0:.2f}\nML = {1:.2f}'.format(h_x, ml))


if __name__ == '__main__':
    main()
