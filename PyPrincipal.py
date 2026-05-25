# coding: utf-8

"""
- Classe Principal
- Controla entrada/saida dos widgets na tela principal
    conforme as ações principais da aplicação:
    - Novo Registro
    - Pesquisa
    - Alterar
    - Apagar
"""


# ----- Importações ----- #
import sqlite3

import PyIntroDados
import PyPesquisa

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label


# ----- Classe Principal ----- #
class Principal(FloatLayout):

    def __init__(self, **kwargs):
        super().__init__()

        self.cont1 = 0  # ----- Controla WidIntroDados I \ O ----- #
        self.cont2 = 0  # ----- Controla WidPesquisa I \ O ----- #
        self.cont3 = 0  # ----- Controla WidResultadoPesquisa I \ O ----- #

        # ----- Instancia Classe Formulário ----- #
        self.widintrodados = PyIntroDados.WidIntroDados()
        # ----- Instancia Classe Pesquisa ----- #
        self.widpesquisa = PyPesquisa.WidPesquisa()
        # ----- Instancia Classe Resultado da Pesquisa ----- #
        self.widrespesquisa = PyPesquisa.ResPesquisaWid()

        # ----- Variavel da ação desejada dos botões principais ----- #
        # 'Novo Registro' - 'Pesquisa' - 'Alterar Registro' - 'Apagar Registro' #
        self.tipo_acao_principal = None


    def acao_principal(self, tipoacao):

        # ----- Confere se tem um formulário já aberto ----- #
        if self.cont1 == 1:

            self.remove_widget(self.widintrodados)  # Remove wid intro dados
            self.cont1 = 0

        if self.cont2 == 1:

            self.remove_widget(self.widpesquisa)  # Remove wid pesquisa
            self.cont2 = 0

        if self.cont3 == 1:

            self.remove_widget(self.widrespesquisa)  # Remove wid resultado da pesquisa
            self.cont3 = 0

        if self.cont1 == 0:

            if tipoacao == 'Novo Registro':
                self.wid_intro_dados(tipoacao)

            else:
                self.wid_pesquisa(tipoacao)

            self.tipo_acao_principal = tipoacao


            # if tipoacao == 'Alterar Registro':
            #     self.wid_pesquisa(tipoacao)

            # if tipoacao == 'Apagar Registro':
            #     self.wid_pesquisa(tipoacao)

            # if tipoacao == 'Pesquisa':
            #     self.wid_pesquisa(tipoacao)


    # ----- Abre formulario introdução de dados na ação principal ----- #
    def wid_intro_dados(self, tipowid):
        
        # ----- Abre formulario introdução de dados ----- #
        self.add_widget(self.widintrodados)
        self.widintrodados.ids.titulo_widintrodados.text = tipowid  # Titulo formulário
        self.widintrodados.limpa_widintrodados()  # Prepara widgets novo formulário
        self.widintrodados.tipo_acao = tipowid  # Indica a ação desejada             
        self.cont1 = 1


    # ----- Abre widget de pesquisa ----- #
    def wid_pesquisa(self, tipoacao):

        self.add_widget(self.widpesquisa)
        self.widintrodados.limpa_widintrodados()  # Prepara widgets novo formulário
        self.widpesquisa.limpa_widpesquisa()  # Prepara widgets para nova pesquisa
        self.widpesquisa.ids.textopesquisa.text = tipoacao
        self.widpesquisa.tipo_acao_pesq = tipoacao
        
        self.cont2 = 1


    # ----- Opções de wid de resultado da pesquisa ----- #
    def opcoes_pesquisa(self, texto):

        if self.tipo_acao_principal != 'Pesquisa':
            self.open_wid_intro_dados(texto)

        if self.tipo_acao_principal == 'Pesquisa':
            self.open_wid_res_pesquisa(texto)

    
    # ----- Abre formulario introdução de dados depois da pesquisa ----- #
    def open_wid_intro_dados(self, nome):

        # ----- Confere se tem um formulário já aberto ----- #
        if self.cont1 == 1:

            self.widintrodados.limpa_widintrodados()
            self.remove_widget(self.widintrodados)  # Remove wid intro dados

        self.add_widget(self.widintrodados)
        self.widintrodados.ids.titulo_widintrodados.text = self.widpesquisa.tipo_acao_pesq
        self.widintrodados.tipo_acao = self.widpesquisa.tipo_acao_pesq  # Indica a ação desejada
        self.widintrodados.ids.btn_limpar.disabled = True
        self.widintrodados.inicio_alterar_dados(nome)

        self.cont1 = 1
        

    # ----- Fecha wids ----- #
    def close_wid(self):

        if self.cont1 == 1:
            self.widintrodados.limpa_widintrodados()
            self.remove_widget(self.widintrodados)
            self.cont1 = 0

        if self.cont3 == 1:
            self.remove_widget(self.widrespesquisa)
            self.cont3 = 0


    # ----- Abre wid resultados da pesquisa ----- #
    def open_wid_res_pesquisa(self, texto):

        if self.cont3 == 1:

            self.remove_widget(self.widrespesquisa)
            self.cont3 = 0

        self.add_widget(self.widrespesquisa)
        self.widrespesquisa.resultado_pesq(texto)

        self.cont3 = 1


    # ----- Ações iniciais para apagar registro ----- #
    def apagar_registro(self):

        self.widintrodados.apagar_registro_f()
        self.remove_widget(self.widpesquisa)
        self.remove_widget(self.widintrodados)


# ----- Classes Popups ----- #
class PopupSalvar(Popup):
    pass


class PopupFaltaDados(Popup):
    pass


class PopupConfirmacao(Popup):
    
    # ----- Texto acentuado ----- #
    texto = 'Não'


# ----- Modelo Wid Label ----- #
class WidLabelTexto(Label):

    historico = 'Histórico:'
    certidao = 'Certidão:'
    posicao = 'Posição:'


# ----- Modelo Wid Label resultados ----- #
class WidLabelResultados(Label):
    pass
