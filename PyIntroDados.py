# coding: utf-8

"""
    Modulo utilizado para criar o Widget 'WidIntroDados'
    Ações para 'Salvar' e 'Alterar'

    O Widget vai ser usado para introduzir dados quando:
    - Salvar
    - Alterar
"""

# ----- Importações ----- #

import sqlite3
import os

import PyPrincipal
import PyPesquisa

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

# ----- Path Base de Dados ----- #
db_path = os.path.expanduser(
    "~/Sistema Gestao Escolar/Arquivo Passivo/BDArquivoPassivo.db")


# ----- Classe Formulário ----- #
class WidIntroDados(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__()

        self.cont1 = 0  # Controla wid resultados I \ O
        self.tipo_acao = None  # Variavel da ação desejada dos botões principais

        # ----- Instancia Classe resultados local arquivo ----- #
        self.widresultado1 = WidResultado1()

        # ----- Texto acentuado dos widgets ----- #
        self.ids.lbl_05.text = 'Histórico'
        self.ids.lbl_06.text = 'Certidão de Nascimento'
        self.ids.lbl_08.text = 'Não'
        self.ids.lbl_10.text = 'Não'

    # ----- Prepara o novo formulário de dados ----- #
    def limpa_widintrodados(self):

        # ----- Limpa os widgets do formulário de dados ----- #
        self.ids.txt_input01.focus = True
        self.ids.txt_input01.text = ''
        self.ids.txt_input02.text = ''
        self.ids.txt_input03.text = ''
        self.ids.txt_input04.text = ''
        self.ids.check01.active = False
        self.ids.check02.active = False
        self.ids.check03.active = False
        self.ids.check04.active = False

        self.ids.btn_salvar.disabled = False  # Abilita de novo o botão de salvar
        self.ids.btn_limpar.disabled = False  # Abilita de novo o botão de limpar

        self.ids.btn_salvar.text = '  Salvar'
        self.ids.btn_salvar.color = (0.831, 0.941, 1, 1)

        self.remove_widget(self.widresultado1)  # retira wid resultados

    # ----- Ações do botão salvar ----- #
    def acao_btn_salvar(self):

        # ----- recolha dos dados do formulario ----- #
        aluno = self.ids.txt_input01.text
        cpf = self.ids.txt_input02.text
        rg = self.ids.txt_input03.text
        datanasc = self.ids.txt_input04.text
        result_checkboxes = [
            self.ids.check01.active,
            self.ids.check02.active,
            self.ids.check03.active,
            self.ids.check04.active]

        # ----- Ações do botão salvar ----- #
        if self.tipo_acao == 'Novo Registro':
            self.salvar_dados(aluno, cpf, rg, datanasc, result_checkboxes)

        if self.tipo_acao == 'Alterar Registro':
            self.alterar_dados(aluno, cpf, rg, datanasc, result_checkboxes)

        if self.tipo_acao == 'Apagar Registro':
            # ----- Popup confirmação apagar ----- #
            PyPrincipal.PopupConfirmacao().open()


    # ----- Salva os dados ----- #
    def salvar_dados(self, aluno, cpf, rg, datanasc, result_checkboxes):

        # ----- Confere se está preenchido corretamente o formulário ----- #
        if aluno != '' \
                and True in result_checkboxes[0:2] \
                and True in result_checkboxes[2:]:

            conexao = sqlite3.connect(db_path)
            cursor = conexao.cursor()

            # ----- Confere se o aluno já está registrado ----- #
            cursor.execute(''' SELECT NOME FROM ARQUIVOPASS
                        WHERE NOME = '{}'
                    '''.format(aluno))

            if cursor.fetchone() is not None:

                # ----- Popup aviso aluno já cadastrado ----- #
                PyPrincipal.PopupSalvar(  # Popup aluno já está registrado
                    title='O Aluno(a) \n já está cadastrado',
                    separator_color=[1, 0, 0, 1]).open()

            # ----- Inicio Salvar Dados ----- #
            else:

                ''' - Os registros são arquivados em grupos de 30 registros
                      com a primeira letra de cada aluno
                    - O resultado é: Grupo, nº do grupo,
                      nº posição no grupo e numero do protocolo (=id)
                '''

                limpa_grupo = aluno.strip()  # retira espaços vazios
                grupo = limpa_grupo[0].upper()  # Primeira letra maiuscula nome

                # ----- Numero de protocolo = id ----- #
                cursor.execute(''' SELECT MAX(IDARQPASS) FROM ARQUIVOPASS ''')

                protocolo_max = cursor.fetchone()

                if protocolo_max[0] == None:  # No caso de ser o 1º registro

                    protocolo = 1

                else:
                    protocolo = protocolo_max[0] + 1

                # ----- Maior numero do grupo ----- #
                cursor.execute(''' SELECT MAX(NUMGRUPO) FROM ARQUIVOPASS
                                    WHERE GRUPO = '{}' '''.format(grupo))

                num_grupo_max = cursor.fetchone()

                # ----- Maior numero da posição no grupo ----- #
                cursor.execute(''' SELECT MAX(NUM_NO_GRUPO) FROM ARQUIVOPASS
                                    WHERE NUMGRUPO = '{}' AND GRUPO = '{}' 
                                    '''.format(num_grupo_max[0], grupo))

                posicao_max = cursor.fetchone()

                # ----- Confere se o grupo tem 30 registros ----- #
                if posicao_max[0] == None:

                    num_grupo = 1
                    posicao = 1

                elif posicao_max[0] < 30:

                    num_grupo = num_grupo_max[0]
                    posicao = posicao_max[0] + 1

                else:
                    num_grupo = num_grupo_max[0] + 1
                    posicao = 1

                # ----- Registra o aluno ----- #
                insert = ''' INSERT INTO ARQUIVOPASS
                            (NOME, CPF, RG, DATANASC, HISTORICO, CERTINASC,
                            GRUPO, NUMGRUPO, NUM_NO_GRUPO) '''

                values1 = (aluno.strip(), cpf, rg, datanasc,
                           result_checkboxes[0], result_checkboxes[2],
                           grupo, num_grupo, posicao)

                values2 = ''' VALUES
                            ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')
                            '''.format(*values1)

                cursor.execute(insert + ' ' + values2)
                conexao.commit()
                conexao.close()

                # ----- Insere o widget de resultados ----- #
                self.add_widget(self.widresultado1)
                self.widresultado1.ids.lbl_titulo.text = 'Cadastrado com sucesso'
                self.widresultado1.ids.lbl_pasta.text = '{} - {}'.format(grupo, num_grupo)
                self.widresultado1.ids.lbl_posicao.text = str(posicao)
                self.widresultado1.ids.lbl_protocolo.text = 'AP.{}'.format(protocolo)

                # ----- Desabilita o botão de salvar ----- #
                self.ids.btn_salvar.disabled = True
                self.ids.btn_salvar.background_disabled_normal = 'Images/btn_azulDisable60.png'

        # ----- Popups falta no preenchimento do formulário ----- #
        else:
            self.popups_aviso(aluno, result_checkboxes)


    # ----- Recolhe os dados já registrados ----- #
    def inicio_alterar_dados(self, nome):

        self.add_widget(self.widresultado1)

        if self.tipo_acao == 'Alterar Registro':
            self.ids.btn_salvar.text = '  Alterar'
            self.ids.btn_salvar.color = (0.831, 0.941, 1, 1)

        if self.tipo_acao == 'Apagar Registro':
            self.ids.btn_salvar.text = '  Apagar'
            self.ids.btn_salvar.color = (1, 0, 0, 1)

        conexao = sqlite3.connect(db_path)
        cursor = conexao.cursor()

        cursor.execute(''' SELECT IDARQPASS, NOME, CPF, RG, DATANASC, HISTORICO, CERTINASC,
                            GRUPO, NUMGRUPO, NUM_NO_GRUPO
                            FROM ARQUIVOPASS
                            WHERE NOME = '{}' '''.format(nome))

        # ----- Dados do formulario ----- #
        for res in cursor:

            self.ids.txt_input01.text = str(res[1])
            self.ids.txt_input02.text = str(res[2])
            self.ids.txt_input03.text = str(res[3])
            self.ids.txt_input04.text = str(res[4])

            if res[5] == 'True':
                self.ids.check01.active = True
            if res[5] == 'False':
                self.ids.check02.active = True
            if res[6] == 'True':
                self.ids.check03.active = True
            if res[6] == 'False':
                self.ids.check04.active = True
            
            self.widresultado1.ids.lbl_titulo.text = 'Local do Registro'
            self.widresultado1.ids.lbl_pasta.text = '{} - {}'.format(str(res[7]), str(res[8]))
            self.widresultado1.ids.lbl_posicao.text = str(res[9])
            self.widresultado1.ids.lbl_protocolo.text = 'AP.{}'.format(str(res[0]))


    def alterar_dados(self, aluno, cpf, rg, datanasc, result_checkboxes):

        # ----- id do registro para alteração ----- #
        id_reg = self.widresultado1.ids.lbl_protocolo.text[3:]

        # ----- Confere se está preenchido corretamente o formulário ----- #
        if aluno != '' \
                and True in result_checkboxes[0:2] \
                and True in result_checkboxes[2:]:

            conexao = sqlite3.connect(db_path)
            cursor = conexao.cursor()

            cursor.execute('''UPDATE ARQUIVOPASS
                                SET (NOME, CPF, RG, DATANASC, HISTORICO, CERTINASC)
                                = ('{}', '{}', '{}', '{}', '{}', '{}')
                                WHERE IDARQPASS = '{}'
                                '''.format(aluno, cpf, rg, datanasc, \
                                    result_checkboxes[0], result_checkboxes[2], id_reg))

            conexao.commit()
            conexao.close()

            # ----- Popup alterado com sucesso ----- #
            PyPrincipal.PopupSalvar(
                title='Registro alterado \ncom sucesso',
                separator_color=[0, 1, 0, 1]).open()

            # ----- Desabilita o botão de salvar ----- #
            self.ids.btn_salvar.disabled = True
            self.ids.btn_salvar.background_disabled_normal = 'Images/btn_azulDisable60.png'

        # ----- Popups falta no preenchimento do formulário ----- #
        else:
            self.popups_aviso(aluno, result_checkboxes)


    def apagar_registro_f(self):

        # ----- id do registro para alteração ----- #
        id_reg = self.widresultado1.ids.lbl_protocolo.text[3:]

        conexao = sqlite3.connect(db_path)
        cursor = conexao.cursor()

        cursor.execute(''' DELETE FROM ARQUIVOPASS
                            WHERE IDARQPASS = '{}' '''.format(id_reg))

        conexao.commit()
        conexao.close()

        # ----- Popup alterado com sucesso ----- #
        PyPrincipal.PopupSalvar(
            title='Protocolo - {} \napagado com sucesso'.format(
                self.widresultado1.ids.lbl_protocolo.text),
            separator_color=[0, 1, 0, 1]).open()


    # ----- Popups falta no preenchimento do formulário ----- #
    def popups_aviso(self, aluno, result_checkboxes):

        if aluno == '':  # Popup falta nome aluno
            PyPrincipal.PopupFaltaDados(
                pos_hint={'x': .60, 'y': .755}, size_hint=(.50, .02),
                title=(f'? {10 * " "} Nome do Aluno {10 * " "} ?')).open()

        elif not True in result_checkboxes:  # Popup falta historico e certidão
            PyPrincipal.PopupFaltaDados(
                pos_hint={'x': .551, 'y': .526}, size_hint=(.80, .02),
                title=(f'? {12 * " "} ? {40 * " "} ? {12 * " "} ?')).open()

        elif not True in result_checkboxes[0:2]:  # Popup falta historico
            PyPrincipal.PopupFaltaDados(
                pos_hint={'x': .552, 'y': .526}, size_hint=(.10, .02),
                title=(f'? {12 * " "} ?')).open()

        elif not True in result_checkboxes[2:]:  # Popup falta certidão
            PyPrincipal.PopupFaltaDados(
                pos_hint={'x': .768, 'y': .526}, size_hint=(.10, .02),
                title=(f'? {12 * " "} ?')).open()


# ----- Classe resultados local arquivo ----- #
class WidResultado1(BoxLayout):

    # ----- Texto acentuado dos widgets ----- #
    posicao = 'Posição'
