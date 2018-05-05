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

        # Qual API('s) do Google acessaremos
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']  

        # cria uma 'credencial' através do nome de arquivo .JSON
        credentials = ServiceAccountCredentials.from_json_keyfile_name('SpreadsheetExample-f5e69c08620f.json', scope)  

        # (gc --> gspread.client.Client) # Loga com a API google usando uma credencial OAuth2
        gc = gspread.authorize(credentials)      


        # ATRIBUTOS DA INSTANCIA (PROTECTED)
        self._spread = gc.open(planilha)         #  (self.spread --> Spreadsheet)

        # Spreadsheet.worksheet('planilha') é um meth q retorna a worksheet(sub-planilha) de 'planilha'. 
        self._wks_pres = self._spread.worksheet('Presenca')  
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

            self.lst_membros.append(Jogador(nome, pres, gols, ass)) # COMPOSIÇÃO
            time.sleep(2)


    def determinar_pontos(self, data_inicio, data_final):

        # determinando o numero da coluna na worksheet que representa a data inicial
        col_inicial = self._wks_pres.find(data_inicio).col

        # determinando o numero da coluna na worksheet que representa a data final
        col_final = self._wks_pres.find(data_final).col

        # lista de tuplas com as infomações - (nome, gols, ass, pts) - de cada prayer entre as dadas especificas
        lst_pontuacao = []   
            
        for prayer in self.lst_membros: # [Jogador1, ..., JogadorN]

            # numero da linha corresponde ao nome do prayer
            linha = self._wks_pres.find(prayer.nome).row

            # quantidade de gols do prayer entre as datas especificas
            gols = sum([ int(cell.value) for cell in self._wks_gols.range(linha, col_inicial, linha, col_final) if cell.value])

            # quantidade de assistencias do prayer entre as datas especificas
            ass = sum([ int(cell.value) for cell in self._wks_ass.range(linha, col_inicial, linha, col_final) if cell.value])

            # adicionando os dados na lista
            lst_pontuacao.append((prayer.nome, gols, ass, gols + ass))

        # retorna a lista com as informações
        return lst_pontuacao
        
            
    def cadastrar_sumula(self):
        ''' Metodo para cadastrar novos valores para as sub-planilhas '''

        # nova data para cadastrar
        data = input('Data Racha: ')

        # quantidade de data na planilha
        total_datas = len( self._wks_pres.row_values(1))
        
        # add nova data em todas as sub-planilhas
        self._wks_pres.update_cell(1, total_datas + 1, data)
        self._wks_gols.update_cell(1, total_datas + 1, data)
        self._wks_ass.update_cell(1, total_datas + 1, data)

        print('SUMULA')
        
        # percorrendo todos os jogadores presente na planilha
        for player in self.lst_membros:   #[Jogador1, ..., JogadorN]
            
            print ('*---------------------------------------------------------------------------------------------------------*') 

            pres = input('\n%s presente (1-Sim)? '%player.nome)  # jogador presente
            linha = self._wks_pres.find(player.nome).row               # determina a linha na planilha atraves do nome do Jogador

            # se o prayer ñ está presente pule para o proximo prayer
            if not pres:
                continue

            # Prayer presente:
            gols = input('\n%s Gols: ' %player.nome)            # quantidade de gols

            # se o prayer tem gol, então:
            if gols:
                player.gols += int(gols)    # atualiza o atributo gols do objeto prayer em questão
            
            assist = input('\n%s Assistências: ' %player.nome)  # quantidade de assistencias

            # se o prayer tem assistencias, então:
            if assist:
                player.assistencias += int(assist)  # atualiza o atributo assistencias do objeto prayer em questão


            print ('*--------------------------------------------------------------------------------------------------------*')

            # atualizando valores  nas planilhas
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
    # DETERMINAR O JOGADOR DO MES

    lst_pontuacao = rcDiscordia.determinar_pontos('19/03', '29/04')

    print('GOLS')
    for tupla in sorted(lst_pontuacao, key = lambda x: x[1], reverse = True):
	print(tupla)
    
    print('ASSISTENCIAS')
    for tupla in sorted(lst_pontuacao, key = lambda x: x[2], reverse = True):
	print(tupla)
    
    print('PONTOS')
    for tupla in sorted(lst_pontuacao, key = lambda x: x[3], reverse = True):
	print(tupla)
	
    '''


    
