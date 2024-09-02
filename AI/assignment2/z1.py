from pyparsing import line
from nonograms import Nonogram


def parse_line_ints(line): return (int(s) for s in line.strip().split())


def load_input():
    # n, m = parse_line_ints(input())
    # row_c = tuple(tuple(parse_line_ints(input())) for _ in range(n))
    # col_c = tuple(tuple(parse_line_ints(input())) for _ in range(m))

    with open('zad_input.txt', 'r') as f:

        lines = f.readlines()

        # print(f"lines: {lines[0].strip().split()} m=?")

        n = int(lines[0].strip().split()[0])
        m = int(lines[0].strip().split()[1])

        row_c = tuple(tuple(parse_line_ints( lines[i+1] )) for i in range(n))
        col_c = tuple(tuple(parse_line_ints( lines[j+n+1] )) for j in range(m))

        # n, m = parse_line_ints()
        # row_c = tuple(tuple(parse_line_ints(input())) for _ in range(n))
        # col_c = tuple(tuple(parse_line_ints(input())) for _ in range(m))

        # print(n,m, file=f)
        # for ll in [row_c, col_c]:
        #     for l in ll:
        #         print(*l, file=f)

    # print(f"rows= {row_c}, columns = {col_c}")
    return row_c, col_c


if __name__ == '__main__':

    with open('zad_output.txt', 'w') as f:

       f.write( Nonogram(*load_input()).solve(print_all=0).return_matrix() )
