"""
Função principal do projeto Humanoide RoboIME 2021

Tomada de decisão para transição entre os estados
Feita para ser utilizada em Raspberry Pi
Segunda versao

    OBSERVAÇÕES:
    

Baseado em main_INTEL_humanoid_2020
@autores: 
"""

#Bibliotecas 

from time import *
import numpy as np
import math
import classes
import funcoes


#Variaveis auxiliares, a velocidade esta em cm/seg
#velocidade = ???                
distancialimite = 46.0
angulo_limite = 10.0
intervalo_alinhamento = 5
largura_do_robo = 25.0


ANDAR="0"                 
GIRAR_ESQUERDA="1"        
GIRAR_DIREITA="2"         
PARAR="3"
SUBIR = "4"
DESCER = "5"
# Configuracoes iniciais

myrio = classes.Classe_porta_serial()
sensor_distancia = classes.Classe_distancia()
camera = classes.Classe_camera()
estado = classes.Classe_estado(myrio)

#Funcao main

def Loop_obstaculo():
    t_0 = time()
    t_1 = intervalo_alinhamento + t_0
    while True:
        print("Estado padrao")
        estado.Trocar_estado(ANDAR, myrio)  
        print(estado)
        ########################################### Checando proximidade de obstáculo ##########################################

        if sensor_distancia.Get_distance() <= distancialimite:
            print ("obstaculo detectado")
            estado.Trocar_estado(PARAR, myrio)
            print(estado)
            estado.Trocar_estado(funcoes.decisao_desvio(camera), myrio)
            print(estado)
            
            if (estado.atual == GIRAR_ESQUERDA or estado.atual == GIRAR_DIREITA):            
                estado.Trocar_estado(funcoes.quando_parar_de_girar(sensor_distancia), myrio)    
                print(estado)
                estado.Trocar_estado(ANDAR, myrio)
                print(estado)
                estado.Trocar_estado(funcoes.quando_parar_de_andar_visaocomp(sensor_distancia, velocidade, largura_do_robo), myrio)
                print(estado)
                print("obstaculo ultrapassado")
            t_1 = time()

        ########################################### Checando alinhamento com a pista ###########################################
        if t_1 - t_0 >= intervalo_alinhamento:
            estado.Trocar_estado(funcoes.checar_alinhamento_pista(), myrio) #PARAR, GIRAR_ESQUERDA ou GIRAR_DIREITA
            print(estado)
            while estado.Obter_estado_atual() != PARAR: 
                print("desalinhado com a pista")
                estado.Trocar_estado(funcoes.checar_alinhamento_pista(), myrio)
                print(estado)
                sleep(0.5)
            print("alinhamento corrigido")
            t_0 = t_1 = time()
        else: t_1 = time()

if __name__ == "__main__":
    try:
        print("Programa rodando... pode ser interrompido usando CTRL+C")
        Loop_obstaculo()
    except KeyboardInterrupt:
        print(" CTRL+C detectado. O loop foi interrompido.")
    estado.Trocar_estado(PARAR, myrio)
    print(estado)