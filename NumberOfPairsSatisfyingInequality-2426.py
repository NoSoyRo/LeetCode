from typing import Optional, List

class _Node:
    __slots__ = ("left", "right", "sum")
    def __init__(self):
        self.left: Optional["_Node"] = None
        self.right: Optional["_Node"] = None
        self.sum: int = 0  # frecuencia total en este intervalo

class DynamicSegTree:
    """
    Árbol de segmentos dinámico para contar frecuencias de enteros en [lo, hi].
    Soporta:
      - add(x, delta): agrega delta a la frecuencia del valor x
      - sum_range(L, R): suma de frecuencias en [L, R]
    """
    def __init__(self, lo: int, hi: int):
        assert lo <= hi, "rango inválido para el árbol"
        self.lo = lo
        self.hi = hi
        self.root: Optional[_Node] = None

    def add(self, x: int, delta: int = 1) -> None:
        if x < self.lo or x > self.hi:
            return  # fuera de rango, no debería suceder si usamos el mismo [lo,hi]
        self.root = self._add(self.root, self.lo, self.hi, x, delta)

    def _add(self, node: Optional[_Node], L: int, R: int, x: int, delta: int) -> _Node:
        if node is None:
            node = _Node()
        node.sum += delta
        if L == R:
            return node
        mid = (L + R) // 2
        if x <= mid:
            node.left = self._add(node.left, L, mid, x, delta)
        else:
            node.right = self._add(node.right, mid + 1, R, x, delta)
        return node

    def sum_range(self, L: int, R: int) -> int:
        if R < self.lo or L > self.hi or L > R:
            return 0
        L = max(L, self.lo)
        R = min(R, self.hi)
        return self._sum(self.root, self.lo, self.hi, L, R)

    def _sum(self, node: Optional[_Node], L: int, R: int, ql: int, qr: int) -> int:
        if node is None or ql > R or qr < L:
            return 0
        if ql <= L and R <= qr:
            return node.sum
        mid = (L + R) // 2
        return self._sum(node.left, L, mid, ql, qr) + \
               self._sum(node.right, mid + 1, R, ql, qr)


def count_pairs_no_compression(nums1: List[int], nums2: List[int], diff: int) -> int:
    """
    Cuenta pares (i, j) con i < j y nums1[i] - nums1[j] <= nums2[i] - nums2[j] + diff,
    usando Segment Tree dinámico SIN compresión de coordenadas.

    Idea:
      a[k] = nums1[k] - nums2[k]
      condición ↔ a[i] <= a[j] + diff
    Recorremos j de 0..n-1 y contamos cuántos i<j cumplen a[i] ≤ a[j]+diff.
    """
    n = len(nums1)
    if n == 0:
        return 0

    a = [x - y for x, y in zip(nums1, nums2)]
    lo, hi = min(a), max(a)

    seg = DynamicSegTree(lo, hi)
    total = 0

    for aj in a:
        T = aj + diff
        # contamos cuántos a[i] ≤ T entre los ya insertados (i < j)
        total += seg.sum_range(lo, T)
        # insertamos a[j] para futuros índices
        seg.add(aj, 1)

    return total


# ----------------- Ejemplo pequeño -----------------
if __name__ == "__main__":
    nums1 = [3, 2, 5]
    nums2 = [2, 2, 1]
    diff = 1
    print(count_pairs_no_compression(nums1, nums2, diff))  # debería imprimir 3
