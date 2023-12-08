class A:
    def __init__(self, test_val: int):
        self.t = test_val

    def test(self, expected: int) -> bool:
        """
        Test method.

        :return:
        """
        return expected == self.t


class C(A):
    ...


class D:
    ...


class E(D, A):
    ...
