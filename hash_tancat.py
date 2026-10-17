# Estats d'una posició de la taula (hash tancat). NO canvieu aquests valors.
LLIURE = "L"
OCUPAT = "O"
ESBORRAT = "B"


class MyHashMap:
    """Taula de hash amb adreçament obert i sondeig lineal."""

    def __init__(self, cap: int = 13):
        # Cada posició s'inicialitza a [None, None, LLIURE]
        self._table = [[None, None, LLIURE] for _ in range(cap)]
        self._n = 0

    def _hash_function(self, key: int) -> int:
        return key % len(self._table)

    def _find(self, key: int):
        """Mètode auxiliar que retorna l'índex on es troba la clau o None si no hi és."""
        m = len(self._table)
        h = self._hash_function(key)

        for i in range(m):
            idx = (h + i) % m
            entry = self._table[idx]
            estat = entry[2]

            if estat == LLIURE:
                # Si trobem una posició LLIURE, la clau no és a la taula
                return None
            elif estat == OCUPAT and entry[0] == key:
                return idx
            # Si és ESBORRAT o OCUPAT amb una altra clau, continuem el sondeig

        return None

    def put(self, key: int, value: int) -> None:
        m = len(self._table)
        h = self._hash_function(key)

        first_deleted = None

        for i in range(m):
            idx = (h + i) % m
            entry = self._table[idx]
            estat = entry[2]

            if estat == OCUPAT:
                if entry[0] == key:
                    # La clau ja existia: actualitzem valor sense canviar n
                    entry[1] = value
                    return
            elif estat == ESBORRAT:
                # Guardem la primera posició ESBORRAT per si cal inserir
                if first_deleted is None:
                    first_deleted = idx
            elif estat == LLIURE:
                # Arribem a LLIURE: la clau segur que no és a la taula
                target_idx = first_deleted if first_deleted is not None else idx
                self._table[target_idx] = [key, value, OCUPAT]
                self._n += 1

                # Comprovem el factor de càrrega
                if self._n > len(self._table) // 2:
                    self._resize(2 * len(self._table) - 1)
                return

        # Si hem recorregut tota la taula (m posicions) sense trobar LLIURE
        if first_deleted is not None:
            self._table[first_deleted] = [key, value, OCUPAT]
            self._n += 1
            if self._n > len(self._table) // 2:
                self._resize(2 * len(self._table) - 1)

    def get(self, key: int) -> int:
        idx = self._find(key)
        if idx is not None:
            return self._table[idx][1]
        return -1

    def remove(self, key: int) -> None:
        idx = self._find(key)
        if idx is not None:
            self._table[idx] = [None, None, ESBORRAT]
            self._n -= 1

    def _resize(self, c: int) -> None:
        old_table = self._table
        self._table = [[None, None, LLIURE] for _ in range(c)]
        self._n = 0

        # Rehashing només dels elements OCUPAT
        for entry in old_table:
            if entry[2] == OCUPAT:
                self.put(entry[0], entry[1])

    def __len__(self) -> int:
        return self._n
