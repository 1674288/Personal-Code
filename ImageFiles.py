# -*- coding: utf-8 -*-
"""
ImageFiles.py : ** REQUIRED ** El vostre codi de la classe ImageFiles.

Aquesta classe s'encarrega de gestionar el llistat d'arxius PNG dins la col·lecció d'imatges.

Funcionalitat:
    - Recórrer el filesystem a partir de ROOT_DIR per trobar tots els arxius PNG
    - Mantenir una representació en memòria dels arxius presents
    - Detectar quins arxius s'han afegit o eliminat des de l'última lectura

Mètodes a implementar:
    - reload_fs(path: str) -> None
        Recorre el directori especificat i actualitza la llista d'arxius PNG.
        Detecta els arxius nous i els que s'han eliminat.

    - files_added() -> list
        Retorna una llista (de strings) amb els paths relatius dels arxius
        que s'han afegit des de l'última crida a reload_fs().

    - files_removed() -> list
        Retorna una llista (de strings) amb els paths relatius dels arxius
        que s'han eliminat des de l'última crida a reload_fs().

Notes:
    - Els paths han de ser sempre relatius a ROOT_DIR
    - Només considereu arxius amb extensió .png (case-insensitive)
    - Heu de recórrer tots els subdirectoris recursivament
"""


# -*- coding: utf-8 -*-
"""
ImageFiles.py : gestiona el llistat d'arxius PNG de la col·lecció.

Estructura de dades: un set amb els paths relatius actuals. A cada
reload_fs() es compara amb la lectura anterior per saber què s'ha afegit
i què s'ha eliminat (diferència de conjunts).
"""

import os
import cfg


class ImageFiles:

    def __init__(self):
        self._files = set()    # paths relatius presents a l'última lectura
        self._added = []       # canvis de l'última crida a reload_fs()
        self._removed = []

    def reload_fs(self, path: str = None) -> None:
        """Recorre 'path' (per defecte ROOT_DIR) i actualitza la llista."""
        if path is None:
            path = cfg.ROOT_DIR

        found = set()
        for dirpath, _dirs, names in os.walk(path):
            for name in names:
                if name.lower().endswith(".png"):
                    full = os.path.join(dirpath, name)
                    found.add(cfg.get_canonical_pathfile(full))

        self._added = sorted(found - self._files)
        self._removed = sorted(self._files - found)
        self._files = found

    def files_added(self) -> list:
        """Paths relatius afegits des de l'última crida a reload_fs()."""
        return list(self._added)

    def files_removed(self) -> list:
        """Paths relatius eliminats des de l'última crida a reload_fs()."""
        return list(self._removed)

    def get_files(self) -> list:
        """Tots els paths relatius coneguts (mètode auxiliar)."""
        return sorted(self._files)