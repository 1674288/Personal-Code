class MyHashMap:
    """Taula de hash amb encadenament separat i redimensionament dinàmic.

    Cada posició de self._table és:
      - None si cap clau hi ha anat a parar.
      - Una llista (bucket) de parelles [clau, valor] si hi ha elements.
    """

    def __init__(self, cap: int = 13):
        self._table = cap * [None]
        self._n = 0

    def _hash_function(self, key: int) -> int:
        return key % len(self._table)

    # ------------------ Mètodes auxiliars per a buckets ------------------

    def _bucket_get(self, j: int, key: int) -> int:
        bucket = self._table[j]
        if bucket is not None:
            for item in bucket:
                if item[0] == key:
                    return item[1]
        return -1

    def _bucket_put(self, j: int, key: int, value: int) -> None:
        if self._table[j] is None:
            self._table[j] = [[key, value]]
            self._n += 1
        else:
            for item in self._table[j]:
                if item[0] == key:
                    item[1] = value
                    return
            self._table[j].append([key, value])
            self._n += 1

    def _bucket_remove(self, j: int, key: int) -> None:
        bucket = self._table[j]
        if bucket is not None:
            for i, item in enumerate(bucket):
                if item[0] == key:
                    bucket.pop(i)
                    self._n -= 1
                    # Si el bucket queda buit, podem deixar-lo buit o mantenir la llista.
                    # Mantenir la llista buida o deixar None és vàlid; 
                    # si es buida del tot, retornar a None manté la coherència inicial:
                    if len(bucket) == 0:
                        self._table[j] = None
                    return

    # ------------------ Redimensionament (Part 2) ------------------

    def _resize(self, c: int) -> None:
        old_table = self._table
        self._table = c * [None]
        self._n = 0  # Es restablirà amb les crides a _bucket_put

        for bucket in old_table:
            if bucket is not None:
                for key, value in bucket:
                    new_j = self._hash_function(key)
                    self._bucket_put(new_j, key, value)

    # ------------------ Mètodes públics ------------------

    def put(self, key: int, value: int) -> None:
        j = self._hash_function(key)
        self._bucket_put(j, key, value)

        # Condició de redimensionament: factor de càrrega > 0.5
        if self._n > len(self._table) // 2:
            self._resize(2 * len(self._table) - 1)

    def get(self, key: int) -> int:
        j = self._hash_function(key)
        return self._bucket_get(j, key)

    def remove(self, key: int) -> None:
        j = self._hash_function(key)
        self._bucket_remove(j, key)

    def __len__(self) -> int:
        return self._n
