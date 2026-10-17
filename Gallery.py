# -*- coding: utf-8 -*-
"""
Gallery.py : ** REQUIRED ** El vostre codi de la classe Gallery.

Aquesta classe s'encarrega de gestionar galeries d'imatges en format JSON.

Funcionalitat:
    - Llegir galeries des d'arxius JSON
    - Visualitzar totes les imatges d'una galeria
    - Afegir i eliminar imatges de la galeria

Format JSON d'una galeria:
{
  "gallery_name": "Cyberpunk Cities",
  "description": "Collection of futuristic urban landscapes",
  "created_date": "2025-09-30",
  "images": [
    "generated_images/city_001.png",
    "generated_images/city_neon_12.png",
    "generated_images/urban_street_45.png"
  ]
}

Mètodes a implementar:
    - load_file(file: str) -> None
        Llegeix un arxiu JSON amb la definició de la galeria.
        Ha de validar que cada imatge referenciada existeix a la col·lecció.
        Si una imatge no existeix, l'ignora i continua processant.
        Emmagatzema internament els UUID de les imatges vàlides.

    - show() -> None
        Visualitza totes les imatges de la galeria en ordre utilitzant
        ImageViewer.show_image().

    - add_image_at_end(uuid: str) -> None
        Afegeix una imatge al final de la galeria.

    - remove_first_image() -> None
        Elimina la primera imatge de la galeria.

    - remove_last_image() -> None
        Elimina l'última imatge de la galeria.

Notes:
    - Utilitzeu la llibreria json per llegir els arxius
    - Els paths dins el JSON són relatius a ROOT_DIR
    - Cada galeria és un objecte independent (instància de Gallery)
    - Podeu tenir múltiples galeries actives simultàniament
    - Les operacions d'afegir/eliminar són ràpides (no busquen a la llista)
"""
# -*- coding: utf-8 -*-
"""
Gallery.py : gestiona una galeria d'imatges definida en un JSON.

Estructura de dades: un deque (collections) amb els UUID de les imatges en
ordre. Afegir al final i treure del principi o del final són O(1), sense
haver de recórrer ni desplaçar elements com passaria amb una llista.
"""

import json
import os
from collections import deque

import cfg


class Gallery:

    def __init__(self, image_id, image_viewer):
        self._image_id = image_id        # per passar de path a UUID
        self._viewer = image_viewer      # per visualitzar les imatges
        self.name = ""
        self.description = ""
        self.created_date = ""
        self._uuids = deque()

    def load_file(self, file: str) -> None:
        """Llegeix el JSON de la galeria; ignora les imatges que no existeixen."""
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, ValueError) as e:
            print("ERROR: no es pot llegir la galeria {}: {}".format(file, e))
            return

        if not isinstance(data, dict):
            print("ERROR: format de galeria incorrecte: {}".format(file))
            return

        self.name = data.get("gallery_name", "")
        self.description = data.get("description", "")
        self.created_date = data.get("created_date", "")

        self._uuids = deque()
        for path in data.get("images", []):
            canon = os.path.normpath(path).replace(os.sep, "/")
            uuid = self._image_id.get_uuid(canon)
            if uuid is None:
                print("AVÍS: imatge inexistent a la col·lecció, s'ignora: {}".format(path))
                continue
            self._uuids.append(uuid)

    def show(self) -> None:
        """Visualitza totes les imatges de la galeria, en ordre."""
        for uuid in self._uuids:
            self._viewer.show_image(uuid, cfg.DISPLAY_MODE)

    def add_image_at_end(self, uuid: str) -> None:
        self._uuids.append(uuid)

    def remove_first_image(self) -> None:
        if self._uuids:
            self._uuids.popleft()

    def remove_last_image(self) -> None:
        if self._uuids:
            self._uuids.pop()

    # ---- mètodes auxiliars ----------------------------------------------

    def load_uuids(self, uuids: list) -> None:
        """Omple la galeria amb una llista d'UUID (p.ex. el resultat d'una cerca)."""
        self._uuids = deque(uuids)

    def get_uuids(self) -> list:
        return list(self._uuids)

    def __len__(self) -> int:
        return len(self._uuids)