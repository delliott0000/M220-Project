from typing import Sequence
from random import choice
from sympy import Matrix


MaybeInt = int | None


print("""
Variables:
    - n: number of dimensions on our vectors (n = 3 might produce (3, 2, -1) as a vector)
    - r: total number of vectors
    - c: range from which to randomly generate vector coordinates
    - d: dimension of the vector subspace of our vectors
We will be able to use this program to look at the relationship between n, r, c and d.
    """)


def get_int_input(string: str) -> int:
    while True:
        value = input(f'Enter an integer value for {string}: ')
        try:
            return int(value)
        except ValueError:
            print('Invalid number. Try again.')


def print_line() -> None:
    """
    Helper function to help us format our console output.
    """

    print('----------------')


def print_matrix(matrix: Matrix) -> None:
    """
    Helper function that allows us to neatly display a matrix in the console.
    """

    for i in range(matrix.rows):
        print(str(matrix.row(i))[9:-3])
    print_line()


def generate_random_vector(n: int, c: Sequence[int] = range(10)) -> tuple[int, ...]:
    """
    Randomly generates and returns an n-dimensional vector in ℝ.

    Vectors here are modelled as an n-sized tuple of integers.

    Each individual coordinate is limited to the range c.
    """

    if n < 1:
        raise ValueError('n must be greater than or equal to 1')

    return tuple(choice(c) for _ in range(n))


def vectors_to_matrix(vectors: list[tuple[int, ...]], _t: bool = True) -> Matrix:
    """
    Takes an r-sized list of n-dimensional vectors.

    Returns an n x r matrix where the given vectors are the column vectors of the matrix.
    """

    m = Matrix(vectors)
    if _t:
        # Returning the transpose by default because of how `Matrix` constructor handles passes arguments
        return m.transpose()
    else:
        return m


def rref(matrix: Matrix) -> Matrix:
    """
    Returns the given matrix in reduced row echelon form (rref).
    """

    return matrix.rref()[0]


def pivot_columns(m: Matrix) -> int:
    """
    Returns the number of pivot columns of the passed matrix `m`, where `m` is assumed to be in rref.

    In other words this is the number of dimensions of `m`'s column space.
    """

    return len(m.columnspace())


def main(
        n: MaybeInt = None,
        r: MaybeInt = None,
        c1: MaybeInt = None,
        c2: MaybeInt = None,
) -> tuple[int, int, Sequence, int]:

    n = n if n is not None else get_int_input('n')
    r = r if r is not None else get_int_input('r')

    c1 = c1 if c1 is not None else get_int_input('lower bound (inclusive)')
    c2 = c2 if c2 is not None else get_int_input('upper bound (exclusive)')
    c = range(c1, c2)

    vectors = [generate_random_vector(n, c) for _ in range(r)]

    print(f'VECTORS: {vectors}')
    print_line()

    matrix = vectors_to_matrix(vectors)
    print('MATRIX:')
    print_matrix(matrix)

    _rref = rref(matrix)
    print('RREF:')
    print_matrix(_rref)

    d = pivot_columns(matrix)
    print(f'Subspace dimension (d) = {d}')
    print_line()

    return n, r, c, d


try:
    while True:
        # Pass values for n, r, c1, c2 here to avoid being prompted for them during runtime
        main()

        start_over = input('Start again [y/n]: ')
        if start_over == 'y':
            continue
        break

except (KeyboardInterrupt, SystemExit):
    pass
