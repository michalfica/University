# def B(i,j):
#     return 'B_%d_%d' % (int(i),int(j))

def B(i, j):
    return f'B_{i}_{j}'

def domains(Vs):
    return [f'{q} in 0..1' for q in Vs]

def constraints(rows, cols): 
    R = len(rows)
    C = len(cols)

    def get_row(i):
        return [B(i,j) for j in range(C)]
    
    def get_col(j):
        return [B(i,j) for i in range(R)]
    
    def get_squares():#lista wszytskich kwadratów na planszy 
        return [(B(i,j),   B(i, j+1),
                 B(i+1,j), B(i+1,j+1)) for i in range(R-1) for j in range(C-1)]

    def get_lines(): #lista wszytskich trójek (trzech kolejnych pół w wierszu lub kolumnie)
        return [(B(i,j), B(i,j+1), B(i,j+2)) for i in range(R) for j in range(C-2)] + \
               [(B(i,j), B(i+1,j), B(i+2,j)) for i in range(R-2) for j in range(C)]
    

    def radars(): #liczba poł burzowych musi się zgadzać w kolumnach i wierszach 
        return [' + '.join(get_row(i)) + ' #= ' + rows[i] for i in range(R)] + \
               [' + '.join(get_col(i)) + ' #= ' + cols[i] for i in range(C)]

    def forbidden(): # zabronione konfiguracje w kwadratach 
                    # plus wynikanie ze srodkowego pola w trójkach 
        return [(b + ' #==> ' + a + ' #\/ ' + c for a, b, c in get_lines())] + \
               [(' + '.join(sq) + ' #\= 3' for sq in get_squares())] + \
               [(f'{a} #/\ {d} #/\ #<==> {b} #/\ {c}' for a, b, c, d in get_squares())]
    return radars() + forbidden()

def print_constraints(cs, indent, d):
    position = indent 
    writeln( (indent -1) * ' ' )
    for c in cs:
        writeln( c + ',')
        position += len(c)
        if position > d:
            position = indent
            writeln('')
            writeln( (indent -1) * ' ')

def storms(rows, cols, triples): 
    writeln(':- use_module(library(clpfd)).')
    
    R = len(rows)
    C = len(cols)
    
    bs = [ B(i,j) for i in range(R) for j in range(C)]
    
    writeln('solve([' + ', '.join(bs) + ']) :- ')

    #CZYM SĄ WIĘZY -> pole planszy B[i][j]
    #JAKA JEST ICH DZIEDZINA: 0 lub 1 

    cs = domains(bs) + list(constraints(rows,cols))
    for i, j, val in triples: #dodaje już określone pola 
        cs.append(f'{B(i,j)} #= {val}')

    print_constraints(cs, 4, 70)

    writeln('    labeling([ff], [' +  ', '.join(bs) + ']).' )
    writeln('')
    writeln(":- tell('prolog_result.txt'), solve(X), write(X), nl, told.")

def writeln(s):
    output.write(s + '\n')

txt = open('zad_input.txt').readlines()
output = open('zad_output.txt', 'w')

rows = txt[0].split()
cols = txt[1].split()
triples = []

for i in range(2, len(txt)):
    if txt[i].strip():
        triples.append(txt[i].split())

storms(rows, cols, triples)            
        

