# coding: utf-8

""" 
    Modulo utilizado para criar o Widget de 'Pesquisa' e 'Resultados da Pesquisa'
    Ações:
    - Pesquisar
    - Escolher um resultado da pesquisa
    - Apresentar resultado da pesquisa
"""


# ----- Importações ----- #
import sqlite3
import os

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView


# ----- Path Base de Dados ----- #
db_path = os.path.expanduser(
    "~/Documents/- Sistema Gestao Escolar -/Arquivo Passivo/BDArquivoPassivo.db")


class WidPesquisa(FloatLayout):
    def __init__(self):
        super().__init__()

        self.contp = 0  # Controla wid para pesquisar I \ O
        self.tipo_acao_pesq = None  # Variavel da ação desejada


    # ----- Limpa os widgets do formulário pesquisa ----- #
    def limpa_widpesquisa(self):

        self.ids.input_pesquisa.focus = True
        self.ids.input_pesquisa.text = ''
        self.ids.box_scrollwid.clear_widgets()
        self.ids.btn_pesquisa.disabled = False
        self.contp = 0

    def pesquisa(self):

        self.input_pesquisa = self.ids.input_pesquisa.text

        if self.contp == 0 and self.input_pesquisa != '':

            self.ids.input_pesquisa.text = ''

            conexao = sqlite3.connect(db_path)
            cursor = conexao.cursor()

            cursor.execute(''' SELECT NOME, CPF, RG
                                FROM ARQUIVOPASS
                                WHERE NOME LIKE '{0}%' OR CPF = '{0}' OR RG = '{0}'
                                ORDER BY NOME
                                '''.format(self.input_pesquisa))

            for res in cursor:
                self.ids.box_scrollwid.add_widget(ScroolWidChild(str(res[0])))

                self.contp = 1

                # ----- Desabilita o botão de salvar ----- #
                self.ids.btn_pesquisa.disabled = True
                self.ids.btn_pesquisa.background_disabled_normal = 'Images/btn_azulDisable60.png'

            conexao.close()


# ----- Resultados da pesquisa ----- #
class ScroolWidChild(Button):

    def __init__(self, texto):
        super().__init__()

        self.text = '{}'.format(texto)


# ----- Scroolview para os resultados da pesquisa ----- #
class Scrollwid(ScrollView):
    pass


# ----- Wid Escolha do resultado da pesquisa ----- #
class ResPesquisaWid(FloatLayout):
    def __init__(self):
        super().__init__()


    def resultado_pesq(self, texto):

        conexao = sqlite3.connect(db_path)
        cursor = conexao.cursor()

        cursor.execute(''' SELECT IDARQPASS, NOME, CPF, RG, DATANASC, HISTORICO,
                            CERTINASC, GRUPO, NUMGRUPO, NUM_NO_GRUPO
                            FROM ARQUIVOPASS
                            WHERE NOME = '{}' '''.format(texto))

        for res in cursor:

            self.ids.lbl_01.text = str(res[1])
            self.ids.lbl_02.text = str(res[4])
            self.ids.lbl_03.text = str(res[2])
            self.ids.lbl_04.text = str(res[3])

            if res[5] == 'True':
                self.ids.lbl_05.text = 'Sim'
            if res[5] == 'False':
                self.ids.lbl_05.text = 'Não'
            if res[6] == 'True':
                self.ids.lbl_06.text = 'Sim'
            if res[6] == 'False':
                self.ids.lbl_06.text = 'Não'

            self.ids.lbl_07.text = '{} - {}'.format(str(res[7]), str(res[8]))
            self.ids.lbl_08.text = str(res[9])
            self.ids.lbl_09.text = 'AP.{}'.format(str(res[0]))

        conexao.close()
