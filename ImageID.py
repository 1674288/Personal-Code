# -*- coding: utf-8 -*-
"""
ImageID.py : ** REQUIRED ** El vostre codi de la classe ImageID.

Aquesta classe s'encarrega de generar i gestionar identificadors únics (UUID)
per a cada imatge de la col·lecció.

Funcionalitat:
    - Generar un UUID únic a partir del path canònic d'un arxiu
    - Mantenir un registre dels UUID generats per evitar col·lisions
    - Permetre consultar i eliminar UUID

Mètodes a implementar:
    - generate_uuid(file: str) -> str
        Genera un UUID únic per a l'arxiu especificat.
        Ha de comprovar que el UUID no estigui ja en ús.
        Si hi ha col·lisió (cas extremadament improbable), retorna None i
        mostra un missatge d'error.

    - get_uuid(file: str) -> str
        Retorna el UUID associat a l'arxiu, si ja ha estat generat.
        Si no existeix, retorna None.

    - remove_uuid(uuid: str) -> None
        Elimina el UUID del registre d'identificadors actius.
        Després d'eliminar-lo, aquest UUID es podrà tornar a utilitzar.

Notes:
    - Els UUID han de seguir el format estàndard (128 bits)
    - Podeu utilitzar la funció cfg.get_uuid() com a base
    - Els UUID s'emmagatzemen com a strings
    - Un UUID només es pot generar una vegada (fins que s'elimini)
"""

# -*- coding: utf-8 -*-
"""
ImageID.py : genera i gestiona els identificadors únics (UUID) de les imatges.

Estructura de dades: dos diccionaris, un per fitxer -> uuid i un altre per
uuid -> fitxer. Així consultar per fitxer (get_uuid) i eliminar per uuid
(remove_uuid) són operacions directes, sense recórrer res.
"""

import cfg


class ImageID:

    def __init__(self):
        self._by_file = {}   # path relatiu -> uuid (str)
        self._by_uuid = {}   # uuid (str) -> path relatiu

    def generate_uuid(self, file: str) -> str:
        """Genera el UUID de 'file' (path relatiu canònic).
        Retorna None i mostra un error si el UUID ja està en ús."""
        uuid = str(cfg.get_uuid(file))

        if uuid in self._by_uuid:
            print("ERROR: el UUID {} ja està en ús (arxiu: {})".format(uuid, file))
            return None

        self._by_file[file] = uuid
        self._by_uuid[uuid] = file
        return uuid

    def get_uuid(self, file: str) -> str:
        """UUID associat a 'file', o None si no s'ha generat."""
        return self._by_file.get(file)

    def remove_uuid(self, uuid: str) -> None:
        """Elimina el UUID del registre; després es podrà tornar a generar."""
        file = self._by_uuid.pop(uuid, None)
        if file is not None:
            self._by_file.pop(file, None)