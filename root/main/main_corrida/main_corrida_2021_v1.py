
#Bibliotecas 

from time import sleep, time

# Configuracoes iniciais

myrio = PortaSerial()
camera = Camera()
estado = Estado(myrio, TEMPO_DO_PASSO)

#Funcao main

def Loop_corrida():
    t_0 = time()
    t_1 =  t_0
    while True:
        print("Andando em frente")
        estado.Trocar_estado(ANDAR)
        sleep(intervalo_caminhada)  # Tentar maximizar intervalo_caminhada quando for botar o robo para andar
        ########################################### Checando alinhamento com a pista ###########################################
        if t_1 - t_0 >= intervalo_alinhamento:
            print("hora de alinhar")
            estado.Trocar_estado(PARAR) ##tirar esse tempo ja que as pausas devem estar embutidas no tirar foto e na troca de estados
            sleep(tempo_para_parar)
            estado.Trocar_estado(funcoes.checar_alinhamento_pista_v2(camera))  # Frente, GIRAR_ESQUERDA ou GIRAR_DIREITA
            numero_de_giradas = 1
            while estado.Obter_estado_atual() == GIRAR_DIREITA or estado.Obter_estado_atual() == GIRAR_ESQUERDA:
                print("desalinhado com a pista, iniciando a ",numero_de_giradas, "a girada")
                sleep(tempo_do_passo[estado.Obter_estado_atual()])
                estado.Trocar_estado(PARAR)
                sleep(tempo_do_passo[PARAR])
                estado.Trocar_estado(funcoes.checar_alinhamento_pista_v2(camera))
                numero_de_giradas+=1
            print("direcao corrigida")
            numero_de_giradas = 1
            print(estado.atual)
            t_0 = t_1 = time()
        else:
            t_1 = time()

def get_camera():
    return camera

def run():
    try:
        print("Programa rodando... pode ser interrompido usando CTRL+C")
        Loop_corrida()
    except KeyboardInterrupt:
        print(" CTRL+C detectado. O loop foi interrompido.")
    estado.Trocar_estado(PARAR)
    print(estado)
