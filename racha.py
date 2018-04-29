''' Teste na Planilha do Racha '''

import gspread          # importar o modulo que gerencia planilhas no Python
import time

from oauth2client.service_account import ServiceAccountCredentials  # classe que cria uma credencial de acesso a uma API

class Jogador:

    # CONSTRUTOR
    def __init__(self, nome, presenca, gols, assistencias):
        ''' (str, int, int, int, int) '''

        # ATRIBUTOS
        self.nome = nome                  # ---> string
        self.presenca = presenca          # ---> int
        self.gols = gols                  # ---> int
        self.assistencias = assistencias   # ---> int


    # metodo especial chamado quando usamos print(obj)
    def __str__(self):

        return 'Atleta: %s \nPresenca: %s \nGols: %s \nAssistencias: %s' %(self.nome, self.presenca, self.gols, self.assistencias)


class Racha:

    def __init__(self, planilha):

        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']  # Qual API('s) do Google acessaremos
        credentials = ServiceAccountCredentials.from_json_keyfile_name('SpreadsheetExample-f5e69c08620f.json', scope)  # cria uma 'credencial' através do nome de arquivo .JSON
        gc = gspread.authorize(credentials)      # (gc --> gspread.client.Client) # Loga com a API google usando uma credencial OAuth2


        # ATRIBUTOS DA INSTANCIA (PROTECTED)
        self._spread = gc.open(planilha)         #  (self.spread --> Spreadsheet)
        self._wks_pres = self._spread.worksheet('Presenca')  # Spreadsheet.worksheet('nome') é um meth q retorna a worksheet(sub-planilha) de 'nome' dado
        self._wks_gols = self._spread.worksheet('Gols')
        self._wks_ass = self._spread.worksheet('Assistencias')


        # ATRIBUTOS DA INSTANCIA ( PUBLICOS )
        self.lst_membros = []
        self._determinarMembros()  # metodo que preenche a lista de membros acima

        self.totalGols = 0
        self.totalAssistencias = 0
        self.lista_jogadorDoMes = []


    def _somar_linha(self, planilha, linha):
        lista = [ int(valor) for valor in planilha.row_values(linha)[1:] if valor ] # lista strings
        return(sum(lista))


    def _determinarMembros(self):

        for num in range(2,50):

            nome = self._wks_pres.cell(num,1).value
            pres = self._somar_linha(self._wks_pres, num)
            gols = self._somar_linha(self._wks_gols, num)
            ass = self._somar_linha(self._wks_ass, num)

            self.lst_membros.append( Jogador(nome, pres, gols, ass )) # COMPOSIÇÃO

    def atualizar_dados(self):
        ''' Metodo ao ser chamado para atualizar os dados quando cadastramos uma sumula '''
        pass

    def cadastrar_sumula(self):

        # nova data para cadastrar
        data = input('Data Racha: ')

        # quantidade de data na planilha
        total_datas = len( self._wks_pres.row_values(1))
        
        # add nova data em todas as sub-planilhas
        self._wks_pres.update_cell(1, total_datas + 1, data)
        self._wks_gols.update_cell(1, total_datas + 1, data)
        self._wks_ass.update_cell(1, total_datas + 1, data)

        print('SUMULA')
        
        # percorrendo todos os membros da planilha
        for player in self.lst_membros:
            
            print ('*---------------------------------------------------------------------------------------------------------*') 

            pres = input('\n%s presente (1-Sim)? '%player.nome)  # jogador presente
            linha = self._wks_pres.find(player.nome).row               # determina a linha na planilha atraves do nome do Jogador

            # se o prayer ñ está presente pule para o proximo prayer
            if not pres:
                continue

            # se o prayer estiver presente:
            gols = input('\n%s Gols: ' %player.nome)            # quantidade de gols
            assist = input('\n%s Assistências: ' %player.nome)  # quantidade de assistencias

            print ('*--------------------------------------------------------------------------------------------------------*')
            
            
            # atualizando valores 
            self._wks_pres.update_cell(linha, total_datas + 1, pres)
            self._wks_gols.update_cell(linha, total_datas + 1, gols)
            self._wks_ass.update_cell(linha, total_datas + 1, assist)

        print('FIM SUMULA')


    # MOSTRAR OS GOLS DOS JOGADORES EM FORMA DESCENDENTE
    def show_gols(self):

        print('*----------------------------------   GOLS       -------------------------------------------------*')
        
        lista_artilheiro = sorted(self.lst_membros, key = lambda x: x.gols, reverse=True) 

        for (num,player) in enumerate(lista_artilheiro):
            print('%sº Colocado:\n' %(num+1), player)
            print('\n')

        print('*----------------------------------  FIM GOLS    -------------------------------------------------*')


    # MOSTRAR AS ASSISTENCIAS DOS JOGADORES DESCENDENTE
    def show_assistencias(self):

        print('*----------------------------------   ASSISTÊNCIAS   ---------------------------------------------*')

        lista_garcom = sorted(self.lst_membros, key = lambda x: x.assistencias, reverse=True)
        
        for (num, player) in enumerate(lista_garcom):
            print('%sº COLOCADO:\n' %(num+1), player)
            print('\n')

        print('*----------------------------------  FIM ASSISTENCIAS  --------------------------------------------*')



    def show_presenca(self):

        print('*----------------------------------   PRESENÇA   ---------------------------------------------*')

        lista_presenca = sorted(self.lst_membros, key = lambda x: x.presenca, reverse=True)

        for (num, player) in enumerate(lista_presenca):
            print('%sº COLOCADO:\n' %(num+1), player)
            print('\n')

        print('*----------------------------------  FIM PRESENÇA  --------------------------------------------*')


    
    def mostrar_golsTotais(self):
        
        for player in self.lst_membros:
            self.totalGols += player.gols

        print('Total de Gols: %s' %self.totalGols)


    def mostrar_assistenciasTotais(self):
        
        for player in self.lst_membros:
            self.totalAssistencias += player.assistencias

        print('Total de Assistencias: %s' %self.totalAssistencias)
            

    # METODO ESPECIAL QUANDO CHAMAMOS PRINT
    def __str__(self):

        ps = ''

        for player in self.lst_membros:
            ps += str(player) + '\n'

        return ps

        
if __name__ == '__main__':

    rcDiscordia = Racha('Racha2018Teste')


'''
#print(spread.worksheets())

# lista de membros
lst_membros = []

# Spreadsheet.worksheet('nome') é um meth q retorna a worksheet(sub-planilha) de 'nome' dado
wks_pres = spread.worksheet('Presenca')
wks_gols = spread.worksheet('Gols')
wks_ass = spread.worksheet('Assistencias')


# metodo para calcular gols
def somar_linha(planilha, linha):

    lstGols = [ int(valor) for valor in planilha.row_values(linha)[1:] if valor ] # lista strings
    return(sum(lstGols))
'''

'''
for num in range(2,25):
    
    nome = wks_pres.cell(num,1).value
    pres = somar_linha(wks_pres, num)
    gols = somar_linha(wks_gols, num)
    ass = somar_linha(wks_ass, num)
    lst_membros.append( Jogador(nome, pres, gols, ass ))

'''

''' Funcionando

for player in lst_membros:
    print(player)


print('\n\n\n GOLS')

lista_artilheiro = sorted(lst_membros, key = lambda x: x.gols, reverse = True)

for player in lista_artilheiro:
    print(player)


print('\n\n\n ASSISTÊNCIAS')
lista_garcom = sorted(lst_membros, key = lambda x: x.assistencias, reverse = True)

for player in lista_garcom:
    print(player)

'''  


'''
def cadastrar_sumula():

    # nova data para cadastrar
    data = input('Data Racha: ')

    # quantidade de data na planilha
    total_datas = len( wks_pres.row_values(1))
    
    # add nova data em todas as sub-planilhas
    wks_pres.update_cell(1, total_datas + 1, data)
    wks_gols.update_cell(1, total_datas + 1, data)
    wks_ass.update_cell(1, total_datas + 1, data)

    # percorrendo todos os membros da planilha
    for player in lst_membros:

        pres = input('\n%s presente (1-Sim)? '%player.nome)  # jogador presente
        linha = wks_pres.find(player.nome).row               # determina a linha na planilha atraves do nome do Jogador

        # se o prayer ñ está presente pule para o proximo prayer
        if not pres:
            continue

        # se o prayer estiver presente:
        gols = input('\n%s Gols: ' %player.nome)            # quantidade de gols
        assist = input('\n%s Assistências: ' %player.nome)  # quantidade de assistencias

        # atualizando valores 
        wks_pres.update_cell(linha, total_datas + 1, pres)
        wks_gols.update_cell(linha, total_datas + 1, gols)
        wks_ass.update_cell(linha, total_datas + 1, assist)
'''
        

'''
def _conectar(self):

        # Qual API('s) do Google acessaremos
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

        # cria uma 'credencial' através do nome de arquivo .JSON
        credentials = ServiceAccountCredentials.from_json_keyfile_name('SpreadsheetExample-f5e69c08620f.json', scope)

        # Loga com a API google usando uma credencial OAuth2
        gc = gspread.authorize(credentials)      # gc ----> gspread.client.Client

        # planilha (Spreadsheet)
        return gc.open('Racha2018Teste') # retorna um Spreadsheet    
        #spread = gc.open('Racha2018Teste') # spread ---> Spreadsheet
'''

