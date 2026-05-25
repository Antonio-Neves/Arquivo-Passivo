# coding: utf-8

#################################
#       Arquivo Passivo         #
#                               #
# Author: António Silva Neves   #
#           AN Informática      #
#################################

"""
- Classe APP
- Cria pastas
- Cria Base de Dados
"""

# ----- Importações iniciais ----- #
import kivy
kivy.require('1.11.1')

from kivy import Config
import os
import platform

# ----- Soluciona problemas de OpenGL e placas graficas antigas em windows -- #
if platform.system() == 'Windows':

    os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
    Config.set('graphics', 'multisamples', '0')

# ----- Necessário para Video e Audio no Linux----- #
if platform.system() == 'Linux':

    os.environ['KIVY_VIDEO'] = 'ffpyplayer'

# ----- Importações ----- #
Config.set('graphics', 'window_state', 'maximized')
Config.set('graphics', 'resizable', True)
Config.set('kivy', 'exit_on_escape', '0')
#Config.set('graphics', 'minimum_width', 1024)
#Config.set('graphics', 'minimum_height', 700)

import sqlite3
import PyPrincipal
from kivy.app import App

# ----- Cria pastas ----- #
try:
    os.mkdir(os.path.expanduser(
        "~/Sistema Gestao Escolar"))
    os.mkdir(os.path.expanduser(
        "~/Sistema Gestao Escolar/Arquivo Passivo"))
except:
    pass


# ----- Extrutura Base de Dados ----- #
def cria_basedados(path):

    conexao = sqlite3.connect(path)
    cursor = conexao.cursor()

    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS ARQUIVOPASS(
        IDARQPASS   INTEGER PRIMARY KEY,
        NOME        TEXT    COLLATE NOCASE,
        CPF         TEXT    COLLATE NOCASE,
        RG          TEXT    COLLATE NOCASE,
        DATANASC    TEXT    COLLATE NOCASE,
        HISTORICO   TEXT    COLLATE NOCASE,
        CERTINASC   TEXT    COLLATE NOCASE,
        GRUPO       TEXT    COLLATE NOCASE,
        NUMGRUPO    INTEGER,
        NUM_NO_GRUPO INTEGER
        )
        ''')

    conexao.close()


# ----- Path Base de Dados ----- #
db_path = os.path.expanduser(
    "~/Sistema Gestao Escolar/Arquivo Passivo/BDArquivoPassivo.db")

# ----- Cria Base de Dados ----- #
cria_basedados(db_path)


# ----- Classe App ----- #
class Main(App):

    title = 'Arquivo Passivo'
    icon = 'Images/IconPng.png'

    def build(self):
        return PyPrincipal.Principal()


Main().run()
