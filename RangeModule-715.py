from bisect import bisect_left, bisect_right

class RangeModule:
    def __init__(self):
        # self.iv: lista de intervalos disjuntos [l, r) ordenados por l
        # self.starts: lista paralela solo con los inicios para bisect
        self.iv = []
        self.starts = []

    def addRange(self, left: int, right: int) -> None:
        if left >= right:
            return
        l, r = left, right

        i = bisect_left(self.starts, l)

        # ¿Se solapa/toca el intervalo anterior?
        if i > 0 and self.iv[i - 1][1] >= l:
            i -= 1
            l = min(l, self.iv[i][0])
            r = max(r, self.iv[i][1])

        # Fusiona todos los intervalos que empiezan antes de r
        j = i
        while j < len(self.iv) and self.iv[j][0] <= r:
            r = max(r, self.iv[j][1])
            j += 1

        # Reemplaza los intervalos [i:j] por el fusionado [l, r)
        self.iv[i:j] = [[l, r]]
        self.starts[i:j] = [l]

    def queryRange(self, left: int, right: int) -> bool:
        if left >= right:
            return True
        # Busca el intervalo con inicio <= left
        i = bisect_right(self.starts, left) - 1
        if i < 0:
            return False
        return self.iv[i][1] >= right

    def removeRange(self, left: int, right: int) -> None:
        if left >= right:
            return

        i = bisect_left(self.starts, left)

        # Podría recortar el intervalo anterior si cruza 'left'
        if i > 0 and self.iv[i - 1][1] > left:
            s, e = self.iv[i - 1]
            # Cola izquierda queda [s, left)
            self.iv[i - 1][1] = left
            # Si también hay cola derecha [right, e), insértala y termina
            if e > right:
                self.iv.insert(i, [right, e])
                self.starts.insert(i, right)
                return

        # Elimina/recorta los que empiezan dentro de [left, right)
        while i < len(self.iv) and self.iv[i][0] < right:
            s, e = self.iv[i]
            if e <= right:
                # se elimina completo
                del self.iv[i]
                del self.starts[i]
            else:
                # recorta la parte izquierda: pasa a [right, e)
                self.iv[i][0] = right
                self.starts[i] = right
                break
