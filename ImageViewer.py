# -*- coding: utf-8 -*-
"""
ImageViewer.py : ** REQUIRED ** El vostre codi de la classe ImageViewer.

Aquesta classe s'encarrega de visualitzar imatges i mostrar les seves metadades.

Funcionalitat:
    - Imprimir per pantalla les metadades d'una imatge
    - Mostrar la imatge en pantalla
    - Combinar ambdues accions segons la configuració

Mètodes a implementar:
    - print_image(uuid: str) -> None
        Imprimeix per pantalla totes les metadades de la imatge identificada
        per l'UUID. Ha de mostrar:
        - Dimensions (width x height)
        - Prompt (truncat si és molt llarg)
        - Model
        - Seed
        - CFG Scale
        - Steps
        - Sampler
        - Generated
        - Created Date
        - UUID
        - Path de l'arxiu

    - show_file(file: str) -> None
        Mostra la imatge especificada utilitzant PIL.
        Aquesta funció NO espera que la imatge es tanqui (asíncrona).

    - show_image(uuid: str, mode: int) -> None
        Combina print_image() i show_file() segons el mode especificat:
        - mode 0: només metadades
        - mode 1: metadades + imatge
        - mode 2: només imatge

        Aquesta funció ha d'esperar que l'usuari tanqui la imatge abans
        de retornar (síncrona). Podeu utilitzar input() per fer una pausa.

Notes:
    - Utilitzeu cfg.DISPLAY_MODE per determinar el comportament per defecte
    - Per mostrar imatges: img.show() de PIL
    - Gestioneu les excepcions si la imatge no es pot mostrar
    - El format de sortida ha de ser llegible i ben organitzat
"""

# -*- coding: utf-8 -*-
"""
ImageViewer.py : mostra les metadades i la imatge.

Necessita un objecte ImageData del qual llegeix les metadades ja carregades
en memòria (no torna a llegir el disc).
"""

import os
import cfg
from PIL import Image


class ImageViewer:

    def __init__(self, image_data):
        self._data = image_data

    def print_image(self, uuid: str) -> None:
        """Imprimeix per pantalla les metadades de la imatge."""
        file = self._data.get_file(uuid)
        if file is None:
            print("ERROR: UUID desconegut: {}".format(uuid))
            return

        width, height = self._data.get_dimensions(uuid)
        prompt = self._data.get_prompt(uuid)
        if len(prompt) > 100:
            prompt = prompt[:100] + "..."

        print("Visualitzant [{}]".format(file))
        print(" Dimensions: {}x{} pixels".format(width, height))
        print(" Prompt:     {}".format(prompt))
        print(" Model:      {}".format(self._data.get_model(uuid)))
        print(" Seed:       {}".format(self._data.get_seed(uuid)))
        print(" CFG Scale:  {}".format(self._data.get_cfg_scale(uuid)))
        print(" Steps:      {}".format(self._data.get_steps(uuid)))
        print(" Sampler:    {}".format(self._data.get_sampler(uuid)))
        print(" Generated:  {}".format(self._data.get_generated(uuid)))
        print(" Created:    {}".format(self._data.get_created_date(uuid)))
        print(" UUID:       {}".format(uuid))
        print(" Arxiu:      {}".format(file))

    def show_file(self, file: str) -> None:
        """Mostra la imatge amb PIL sense esperar que es tanqui (asíncrona)."""
        path = file
        if not os.path.isfile(path):
            path = os.path.join(cfg.get_root(), file)   # path relatiu a ROOT_DIR
        try:
            with Image.open(path) as img:
                img.show()
        except Exception as e:
            print("No es pot mostrar la imatge: {}".format(e))

    def show_image(self, uuid: str, mode: int = None) -> None:
        """mode 0: només metadades; 1: metadades + imatge; 2: només imatge.
        Si hi ha imatge, espera que l'usuari premi Enter (síncrona)."""
        if mode is None:
            mode = cfg.DISPLAY_MODE

        if mode < 2:
            self.print_image(uuid)

        if mode > 0:
            file = self._data.get_file(uuid)
            if file is None:
                print("ERROR: UUID desconegut: {}".format(uuid))
                return
            self.show_file(file)
            input("Premi Enter per continuar...")