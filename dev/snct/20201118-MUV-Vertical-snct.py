# -*- coding: utf-8 -*-
#commit alternativo v1.0
#apenas movimento vertical
from numpy import *
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['axes.linewidth'] = 1.1
mpl.rcParams.update({'font.size': 20})
from math import *
import pandas as pd
import os
from datetime import datetime

dt = 0.001        # Step size
g = 9.8        # Acceleration of gravity in m/s² (Latitude 20º, Altitude 500m, segundo Wilson Lopes em VARIAÇÃO DA ACELERAÇÃO DA GRAVIDADE COM A LATITUDE E ALTITUDE)
#-----------------------------#
b = (18720*(10**-9)) # Viscosidade dinâmica em kg/metro*segundo para 30ºC
# ---- Stokes' Law -----------#
p = 1.164             # Densidade do ar em kg/m³  
cd = 0.5               # Drag coefficient of a smooth sphere
#-----------------------------#

#----diretorio---#
raiz='C:/Users/breno/Documents/Drive - ifsp.edu.br/Estudo/PIC/SNCT 2020/repo/data20201118/'

error = 0     #(Debug) Define se o erro será plotado. 0 para não, 1 para sim.

vt_p, f13 = plt.subplots()
yt_p, f14 = plt.subplots()
em_p, f15 = plt.subplots()
emd_p, f16 = plt.subplots()
em_todos, f17 = plt.subplots()

#Note that in this algorithm we adopt the upward path as positive.
    
#12/09 função não usada - compare
#

#12/09 função não usada - theoricf
#

#12/09 função não usada - plot
#

#12/09 função não usada - graphconfig
#

def F(m, f, v):
    return array(-m*g -(f)*v)

#unidades recebidas: m/s², m/s, m, s
def step(a, v, s, dt):
    sn = s + v*dt
    vn = v + a*dt
    return vn, sn


#12/09 remodelado para f(v)=(bv + cv²)
#unidades recebidas: m, m/s, m, kg, adimensional, identidade, identidade
def calcteorico(sinicial, vinicial, diametro, massa):
    global g, b, p, dt
    raio = diametro/2
    time = [0]
    ainicial = -g
    a = [float(ainicial)]
    v = [vinicial]
    s = [sinicial + raio]
    j=0
    while s[j] >= raio:
        
        #06/07 - removido estrutura baseada em N, adicionado append nas matrizes
        time.append(time[j] + dt)
        
        stepr = step(a[0], v[j], s[j], dt)
        #unidades passadas: m/s², m/s, m, s
        
        v.append(stepr[0])

        s.append(stepr[1])

        j+=1
    
    time = array(time[:j])
    a = array(a[:j])
    v = array(v[:j])
    s = array(s[:j])
    return (time, v, s, a)

#Nota 23/10/2020: resolver problema de lançamento vertical. Quando t=0, está pulando o laço while pois s[0] <= 0
def calc(sinicial, vinicial, diametro, massa, cd, termob, termoc):

    global g, b, p, dt
    raio = diametro/2
    area = pi*(raio*raio)
    f = []
    time = [0]
    #ainicial = F(massa, f[0], vinicial)/massa
    a = []
    v = [vinicial]
    s = [sinicial + raio]
    j=0
    while s[j] >= raio:
        
        f.append((b*diametro*termob) + (termoc*0.5*p*cd*area*abs(v[j])))
        
        #06/07 - removido estrutura baseada em N, adicionado append nas matrizes
        time.append(time[j] + dt)
        
        a.append(F(massa, float(f[j]), float(v[j]))/massa)
        
        stepr = step(a[j], v[j], s[j], dt)
        #unidades passadas: m/s², m/s, m, s
        
        v.append(stepr[0])

        s.append(stepr[1])

        j+=1

    time = array(time[:j])
    f = array(f[:j])
    a = array(a[:j])
    v = array(v[:j])
    s = array(s[:j])

    return (time, v, s, f, a)



#12/09 função não usada - configure
#
        
def reynolds(vmax, d):
    re=float((vmax*d)/(1.608*10**-5)) #Maximo Re (velocidade de pico)
    re24=(24/re) #Para Re <<1, coef arrasto é 24/Re
    return re, re24

#12/09 Modificar para adequar ao novo calc()

#recebe m, cm, g, adimensional, string, string
def simulacao(h, vinicial, diametrocm, massag, cd, arrasto, bola): #diametro em cm, massa em g, h em m
    vinicial_kmh=int(vinicial*3.6)
    global b
    h=0
    #vinicial = 0
    #---- Medidas da bola ----#
    diametro = float(diametrocm)/(10**2)     # converte cm em m
    massa = float(massag)/(10**3)           # converte g para kg
    raio = diametro/2
    # ---- Stokes' Law -----------#
    area = pi*(raio*raio)                 # Area de secção transversal em m²
    
    data=[['Bola', bola], ['Velocidade inicial', vinicial], ['Diâmetro', diametro], ['Massa', massa], ['Cross-section', area], ['Coeficiente Arr.', cd], ['Tipo arrasto', arrasto], ['Em inicial', (massa*g*h)]]
    data_array=array(data)
    diretorio=raiz+str(arrasto)+'/'+str(vinicial_kmh)+'/'
    diretorio+=(bola+'/')
    #Acima, define o diretório onde salvar as tabelas
    
    if arrasto == 'p':
        
        t_p, v_p, s_p, f_p, a_p = calc(h, vinicial, diametro, massa, cd, 0, 1)
        #unidades passadas: m, m/s, m, kg, adimensional, identidade, identidade
        
        #Calcula arrasto de pressão
        
        Em_p = zeros([len(v_p), 5])
        
        #Matriz EM:
            #coluna 0 - Energia Cinetica                              #J
            #coluna 1 - Energia potencial gravitacional               #J
            #coluna 2 - Energia mecânica                              #J
            #coluna 3 - Energia dissipada (Em[t=0] - Em[i])           #J
            #coluna 4 - Energia normalizada [0,1] (Em[i]/Em[t=0])     #adimensional
            
        Fr_p = zeros([len(a_p), 1])
        
        #Modificar a Em inicial para mv²/2, pois mgh=0 em t=0
        
        for i in range(len(v_p)):
            vquadrado  = abs(v_p[i])*abs(v_p[i])
            Em_p[i, 0] = (massa*vquadrado*1/2)
            Em_p[i, 1] = massa*g*float(s_p[i])
            Em_p[i, 2] = float(Em_p[i,0])+float(Em_p[i,1])
            Em_p[i, 3] = (massa*vinicial*vinicial*0.5) - float(Em_p[i, 2])
            Em_p[i, 4] = float(Em_p[i, 2])/(massa*vinicial*vinicial*0.5)
            
        for i in range(len(a_p)):
            Fr_p[i]=float(a_p[i])*massa
        
        #12/09 - vmax precisa ser modificado
        vmax_p = max(abs(v_p))
        re_p, re24_p = reynolds(vmax_p, diametro)
        extra_p=array([['Vmax', vmax_p], ['Re', re_p], ['Re/24', re24_p]])
        data_array = vstack((data_array, extra_p))
        
        #Salva tabelas
        
        file_data=diretorio+'setup.txt'
        #pd.DataFrame(data_array).to_csv(file_data, header=None, index=None)
        savetxt(file_data, data_array, delimiter=',', fmt='%s')
        
        file_Em=diretorio+'em.txt'
        #pd.DataFrame(Em_p).to_csv(file_Em, header=None, index=None)
        savetxt(file_Em, Em_p, delimiter=',', fmt='%f')
        
        file_t=diretorio+'t.txt'
        #pd.DataFrame(t_p).to_csv(file_t, header=None, index=None)
        savetxt(file_t, t_p, delimiter=',', fmt='%f')
        
        file_v=diretorio+'v.txt'
        #pd.DataFrame(v_p).to_csv(file_v, header=None, index=None)
        savetxt(file_v, v_p, delimiter=',', fmt='%f')
        
        file_s=diretorio+'s.txt'
        #pd.DataFrame(s_p).to_csv(file_s, header=None, index=None)
        savetxt(file_s, s_p, delimiter=',', fmt='%f')
        
        file_f=diretorio+'f.txt'
        #pd.DataFrame(f_p).to_csv(file_f, header=None, index=None)
        savetxt(file_f, f_p, delimiter=',', fmt='%f')
        
        file_Fr=diretorio+'fr.txt'
        #pd.DataFrame(Fr_p).to_csv(file_Fr, header=None, index=None)
        savetxt(file_Fr, Fr_p, delimiter=',', fmt='%f')
        
        file_a=diretorio+'a.txt'
        #pd.DataFrame(a_p).to_csv(file_a, header=None, index=None)
        savetxt(file_a, a_p, delimiter=',', fmt='%f')
        
        return t_p, v_p, s_p, f_p, a_p, Em_p, data_array
    
    #if v
    #
        
    #if both
    #
    
    #if !=
    #

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print(current_time)
print("Iniciando simulação.")
#bolas=[['Futebol', 22.2, 454], ['Beisebol', 7.3, 145], ['Cricket', 7.2, 163], ['Basquete', 24.3, 600], ['Golfe', 4.3, 46], ['Tênis', 6.5, 58], ['Tênis de mesa', 3.8, 25], ['Voleibol', 21.0, 270], ['Wiffleball', 7.0, 145.3], ['Sepaktakraw', 13.7, 175]]
bolas_arr=[['Voleibol', 21.0, 270], ['Tênis de mesa', 3.8, 25], ['Futebol', 22.2, 454], ['Basquete', 24.3, 600]]
bolas_arr=array(bolas_arr) #unidade bolas: cm, g

#h_tabela = [1000] #unidade: m

#Tabela:
#0ª coluna: bola, string
#1ª coluna: diâmetro, cm
#2ª coluna: massa, g
#3ª coluna: velocidade terminal, m/s
#4ª coluna: Re, adimensional
#5ª coluna: altura máxima
#6ª coluna: energia dissipada %
#7ª coluna: velocidade ao atingir o chão
#8ª coluna: desvio de velocidade (1 - Vfinal/Vfinal_ideal)
#9ª coluna: desvio de altura (1 - altura_real/altura_ideal)
#10ª coluna: tempo de simulação

tabela = [['Voleibol', 21.0, 270, 0, 0, 0, 0, 0, 0, 0, 0], ['Tênis de mesa', 3.8, 25, 0, 0, 0, 0, 0, 0, 0, 0], ['Futebol', 22.2, 454, 0, 0, 0, 0, 0, 0, 0, 0], ['Basquete', 24.3, 600, 0, 0, 0, 0, 0, 0, 0, 0]]
tabela = array(tabela) #unidades tabela: cm, g, m/s, adimensional
#11/09 - Erro: coeficiente b tem valor diferente do esperado.

if not os.path.exists(raiz):
    os.makedirs(raiz)

def vterm_re(massa, diametro, vmax):
    diametro_a = float(diametro)/10**2 #converte cm para m
    massa_a = float(massa)/10**3 #converte g para kg
    raio = (diametro_a)/2
    A = (raio*raio)*pi
    coef_p = p*cd*A
    numerador = 2*massa_a*g
    vterminal = sqrt(numerador/coef_p)
    Re, Re24 = reynolds(vmax, diametro_a)
    return vterminal, Re

veloc_kmh = array([70, 130, 160])
veloc = zeros([len(veloc_kmh), 1])
for i in range(len(veloc_kmh)):
    veloc[i] = veloc_kmh[i]/3.6 #unidade: m/s
tabela_tempos=array([['Voleibol', 0, 0, 0], ['Tênis de mesa', 0, 0, 0], ['Futebol', 0, 0, 0], ['Basquete', 0, 0, 0]])
desvios=array([['Voleibol', 0, 0, 0], ['Tênis de mesa', 0, 0, 0], ['Futebol', 0, 0, 0], ['Basquete', 0, 0, 0]])

for j in range(len(veloc)):
    for i in range(len(bolas_arr)):
        
        #plota para both (f5-f8)
        ########################
        
        #plota para erro (f1-f4)
        #fim plot
        
        #inserir aqui: algoritmo 1 - para igualar os indices das matrizes
        ########################fim_algoritmo
        
        #divide e plot f1-f4
        ########################
        
        #plota para p (f13-f16)
        diretorio=raiz+'p/'+str(veloc_kmh[j])+'/'+(bolas_arr[i, 0])+'/'
        if not os.path.exists(diretorio):
            os.makedirs(diretorio)
        t_p, v_p, s_p, f_p, a_p, Em_p, data_array_p = simulacao(0, veloc[j], bolas_arr[i, 1], bolas_arr[i, 2], 0.45, 'p', bolas_arr[i, 0]) #unidades certas
        
        
#Tabela:
#0ª coluna: bola, string
#1ª coluna: diâmetro, cm
#2ª coluna: massa, g
#3ª coluna: velocidade terminal, m/s
#4ª coluna: Re, adimensional
#5ª coluna: altura máxima
#6ª coluna: energia dissipada %
#7ª coluna: velocidade ao atingir o chão
#8ª coluna: desvio de velocidade (1 - Vfinal/Vfinal_ideal)
#9ª coluna: desvio de altura (1 - altura_real/altura_ideal)
#10ª coluna: tempo de simulação
        tabela[i, 1] = bolas_arr[i, 1] #cm
        tabela[i, 2] = bolas_arr[i, 2] #g
        tabela[i, 3], tabela[i, 4] = vterm_re(float(bolas_arr[i, 2]), float(bolas_arr[i, 1]), float(veloc[j]))
        tabela[i, 5] = float(max(s_p))
        tabela[i, 6] = (1 - float(Em_p[(len(Em_p)-1), 4]))*100
        tabela[i, 7] = float(v_p[len(v_p)-1])
        tabela[i, 8] = (1 - float(v_p[len(v_p)-1])/(-1*float(veloc[j])))*100
        tabela[i, 9] = (1 - float(max(s_p))/(float(veloc[j])*float(veloc[j])*(1/(2*g))))*100
        tabela[i, 10] = float(t_p[len(t_p)-1])
        
        #Desvios
        #1ª coluna: Em
        #2ª coluna: V
        #3ª coluna: altura
        
        desvios[i, 1] = tabela[i, 6]
        desvios[i, 2] = tabela[i, 8]
        desvios[i, 3] = tabela[i, 9]
        
        dirp=raiz+'p/'+str(veloc_kmh[j])+'/'
        savetxt(dirp+'tabela.txt', tabela, delimiter=',', fmt='%s')
        savetxt(dirp+'desvios.txt', desvios, delimiter=',', fmt='%s')
        
        
        energiacte=full([len(t_p), 1], 1)
        f16.plot(t_p, energiacte, 'k--', linewidth='1.6', dashes=(3,8), label='Ideal')
        
        if veloc[j]*3.6 == 70:
            tabela_tempos[i, 1] = t_p[len(t_p)-1] 
        if veloc[j]*3.6 == 130:
            tabela_tempos[i, 2] = t_p[len(t_p)-1] 
        if veloc[j]*3.6 == 160:
            tabela_tempos[i, 3] = t_p[len(t_p)-1] 
        
        #unidades passadas: m, cm, g, adminesional, string, string
        colorcode=''
        if i == 0:  #voleibol
            colorcode='r'
        if i == 1:  #tenis de mesa
            colorcode='b'
        if i == 2:
            colorcode='g'
        if i == 3:
            colorcode='y'
        if i == 4:
            colorcode='c'
        
        diametro_t=float(bolas_arr[i,1])/10**2
        massa_t=float(bolas_arr[i, 2])/10**3
        
        #t_t, v_t, s_t, a_t = calcteorico(h[j], 0, diametro_t, massa_t)

        #f13.plot(t_t, abs(v_t), 'k--', linewidth='0.8', dashes=(3,8))
        #f14.plot(t_t, s_t, 'k--', linewidth='0.8', dashes=(3,8))
        
        f13.plot(t_p, v_p, colorcode, label=bolas_arr[i,0], linewidth='1.6')
        f14.plot(t_p, s_p, colorcode, label=bolas_arr[i,0], linewidth='1.6')
        f15.plot(t_p, Em_p[:, 2], colorcode, label=bolas_arr[i,0], linewidth='1.6')
        f16.plot(t_p, Em_p[:, 4], colorcode, label=bolas_arr[i,0], linewidth='1.6')
        f17.plot(t_p, Em_p[:, 0], 'r', label='Energia cinética', linewidth='1.6')
        f17.plot(t_p, Em_p[:, 1], 'g', label='Energia potencial', linewidth='1.6')
        f17.plot(t_p, Em_p[:, 2], 'b', label='Energia mecânica', linewidth='1.6')
        ########################
        
        #plota para v (f9-f12)
        ########################
        
        #f13.grid()
        #f14.grid()
        #f15.grid()
        #f16.grid()
        
        #titulo erro (f1-f4)
        ######################

        #titulo both (f5-f8)
        ######################
        
        #titulo v (f9-f12)
        ######################
        
        #titulo p (f13-f16)
        f13.set_xlabel('Tempo (s)')
        f14.set_xlabel('Tempo (s)')
        f15.set_xlabel('Tempo (s)')
        f16.set_xlabel('Tempo (s)')
        f17.set_xlabel('Tempo (s)')
        
        f13.set_ylabel('Velocidade (m/s)')
        f14.set_ylabel('Altura (m)')
        f15.set_ylabel('Energia Mecânica (Joules)')
        f16.set_ylabel('Energia ($E_{M}/E_{M_{0}}$)')
        f17.set_ylabel('Energias (Joules)')
        
        em_todos.savefig(dirp+str(bolas_arr[i,0])+'/'+'em_todos.svg', format='svg', dpi=4800, bbox_inches = 'tight', pad_inches = 0)
        f17.cla()
        #valormax_Emp = max(abs(Em_p[:, 4]))+0.001
        #valormin_Emp = min(abs(Em_p[:, 4]))
        #f16.set_ylim(valormin_Emp, valormax_Emp)
            
        ######################
    
    dirp=raiz+'p/'+str(veloc_kmh[j])+'/'
    t_t, v_t, s_t, a_t = calcteorico(0, veloc[j], 0, 0)
    f13.plot(t_t, v_t, 'k--', linewidth='0.9', dashes=(3,8), label='Ideal')
    f14.plot(t_t, s_t, 'k--', linewidth='0.9', dashes=(3,8), label='Ideal')
    
    #salva grafico de erro 
    #
    
    #salva grafico de both
    #
    
    #salva grafico de v
    #
    
    #salva grafico de p
    vt_p.savefig(dirp+'vt_p.svg', format='svg', dpi=4800, bbox_inches = 'tight', pad_inches = 0)
    yt_p.savefig(dirp+'yt_p.svg', format='svg', dpi=4800, bbox_inches = 'tight', pad_inches = 0)
    em_p.savefig(dirp+'em_p.svg', format='svg', dpi=2400, bbox_inches = 'tight', pad_inches = 0)
    emd_p.savefig(dirp+'emd_p.svg', format='svg', dpi=4800, bbox_inches = 'tight', pad_inches = 0)
    
    
    #clear f1-f12
    #
    
    f13.cla()
    f14.cla()
    f15.cla()
    f16.cla()
    f17.cla()
    
savetxt(raiz+'tabela_t.txt', tabela_tempos, delimiter=',', fmt='%s')
    
print("Simulação concluída.")
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print(current_time)
    
#configure(1) #Ao invés de configurar, usa os dados do escopo do programa