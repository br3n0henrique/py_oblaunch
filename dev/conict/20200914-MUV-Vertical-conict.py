# -*- coding: utf-8 -*-
#commit alternativo v1.0
#apenas movimento vertical
from numpy import *
import matplotlib.pyplot as plt
from math import *
import pandas as pd
import os
from datetime import datetime

dt = 0.001        # Step size
g = 9.7848        # Acceleration of gravity in m/s² (Latitude 20º, Altitude 500m, segundo Wilson Lopes em VARIAÇÃO DA ACELERAÇÃO DA GRAVIDADE COM A LATITUDE E ALTITUDE)
#-----------------------------#
b = (18720*(10**-9)) # Viscosidade dinâmica em kg/m . s para 30ºC
# ---- Stokes' Law -----------#
p = 1.164             # Densidade do ar em kg/m³  
cd = 0.45               # Drag coefficient of a smooth sphere
#-----------------------------#

#comentario 14/09:
    #rever unidades
    #terminar o calculo da altura minima
    #plotar curva ideal nos gráficos

error = 0     #(Debug) Define se o erro será plotado. 0 para não, 1 para sim.

vt_erro, f1 = plt.subplots()
yt_erro, f2 = plt.subplots()
em_erro, f3 = plt.subplots()
emd_erro, f4 = plt.subplots()

vt_both, f5 = plt.subplots()
yt_both, f6 = plt.subplots()
em_both, f7 = plt.subplots()
emd_both, f8 = plt.subplots()

vt_v, f9 = plt.subplots()
yt_v, f10 = plt.subplots()
em_v, f11 = plt.subplots()
emd_v, f12 = plt.subplots()

vt_p, f13 = plt.subplots()
yt_p, f14 = plt.subplots()
em_p, f15 = plt.subplots()
emd_p, f16 = plt.subplots()

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

def step(a, v, s, dt):
    sn = s + v*dt
    vn = v + a*dt
    return vn, sn


#12/09 remodelado para f(v)=(bv + cv²)
def calc(sinicial, vinicial, diametro, massa, cd, termob, termoc):
    diametro=float(diametro)
    global g, b, p, dt
    area = pi*((diametro/2)**2)
    f = [((b*diametro*termob) + (termoc*0.5*p*cd*pi*area*abs(vinicial))*vinicial)]
    time = [0]
    a = [F(massa, f[0], vinicial)/massa]
    v = [vinicial]
    s = [sinicial]
    j=0
    while s[j]+(diametro/2) >= 0:
        
        f.append((b*diametro*termob) + (termoc*0.5*p*cd*pi*area*abs(v[j])))
        #f = vstack((f, f2))
        
        #06/07 - removido estrutura baseada em N, adicionado append nas matrizes
        time.append(time[j] + dt)
        
        a.append((F(massa, float(f[j+1]), float(v[j]))/massa))
        
        stepr = step(a[j], v[j], s[j], dt)
        
        v.append(stepr[0])
        #v = vstack((v, v2))
        
        s.append(stepr[1])
        #s = vstack((s, s2))
        j+=1
        
    n=0
    for n in range(len(s)-1):
        if s[n]<=0:
            break
    
    time = array(time[:n])
    f = array(f[:n])
    a = array(a[:n])
    v = array(v[:n])
    s = array(s[:n])
    return (time, v, s, f, a)


#12/09 função não usada - configure
#
        
def reynolds(vmax, d):
    re=float(vmax*d/(1.608*10**-5)) #Maximo Re (velocidade de pico)
    re24=(24/re) #Para Re <<1, coef arrasto é 24/Re
    return re, re24

#12/09 Modificar para adequar ao novo calc()
def simulacao(h, diametro, massa, cd, arrasto, bola): #diametro em cm, massa em g, h em m
    global b
    vinicial = 0
    #---- Medidas da bola ----#
    diametro = float(diametro)/(10**2)     # Transforma diâmetro em m
    massa = float(massa)/(10**3)           # Transforma Massa em kg
    # ---- Stokes' Law -----------#
    area = pi*(diametro/2)*(diametro/2)                   # Area de secção transversal em m²
    
    data=[['Bola', bola], ['Altura', h], ['Diâmetro', diametro], ['Massa', massa], ['Cross-section', area], ['Coeficiente Arr.', cd], ['Tipo arrasto', arrasto], ['Em inicial', (massa*g*h)]]
    data_array=array(data)
    diretorio='C:/Users/breno/Documents/Drive - ifsp.edu.br/Estudo/PIC/11 CONICT/repo/data/'+str(arrasto)+'/'+str(h)+'/'
    diretorio+=(bola+'/')
    #Acima, define o diretório onde salvar as tabelas
    
    if arrasto == 'p':
        
        t_p, v_p, s_p, f_p, a_p = calc(h, vinicial, diametro, massa, cd, 0, 1) #s, m/s, m, m/s2
        #Calcula arrasto de pressão
        
        Em_p = zeros([len(v_p), 5]) #J
        
        #Matriz EM:
            #coluna 0 - Energia Cinetica
            #coluna 1 - Energia potencial gravitacional
            #coluna 2 - Energia mecânica
            #coluna 3 - Energia dissipada (Em[t=0] - Em[i])
            #coluna 4 - Energia dissipada [0,1] (Em[i]/Em[t=0])
        
        for i in range(len(v_p)):
            Em_p[i, 0] = ((massa*float(abs(v_p[i]))**2)/2)
            Em_p[i, 1] = massa*g*s_p[i]
            Em_p[i, 2] = float(Em_p[i,0]+Em_p[i,1])
            Em_p[i, 3] = (massa*g*h) - float(Em_p[i, 2])
            Em_p[i, 4] = Em_p[i, 2]/(massa*g*h)
        
        #12/09 - vmax precisa ser modificado
        vmax_p = max(abs(v_p))
        re_p, re24_p = reynolds(vmax_p, diametro)
        extra_p=array([['Vmax', vmax_p], ['Re', re_p], ['Re/24', re24_p]])
        data_array = vstack((data_array, extra_p))
        
        #Salva tabelas
        
        file_data=diretorio+'setup.csv'
        pd.DataFrame(data_array).to_csv(file_data, header=None, index=None)
        
        file_Em=diretorio+'em.csv'
        pd.DataFrame(Em_p).to_csv(file_Em, header=None, index=None)
        
        file_t=diretorio+'t.csv'
        pd.DataFrame(t_p).to_csv(file_t, header=None, index=None)
        
        file_v=diretorio+'v.csv'
        pd.DataFrame(v_p).to_csv(file_v, header=None, index=None)
        
        file_s=diretorio+'s.csv'
        pd.DataFrame(s_p).to_csv(file_s, header=None, index=None)
        
        file_f=diretorio+'f.csv'
        pd.DataFrame(f_p).to_csv(file_f, header=None, index=None)
        
        file_a=diretorio+'a.csv'
        pd.DataFrame(a_p).to_csv(file_a, header=None, index=None)
        
        return t_p, abs(v_p), s_p, f_p, a_p, Em_p, data_array
    
    if arrasto == 'v':
        
        t_v, v_v, s_v, f_v, a_v = calc(h, vinicial, diametro, massa, cd, 1, 0) #s, m/s, m, m/s2
        #Calcula arrasto de pressão
        
        Em_v = zeros([len(v_v), 5]) #J
        
        #Matriz EM:
            #coluna 0 - Energia Cinetica
            #coluna 1 - Energia potencial gravitacional
            #coluna 2 - Energia mecânica
            #coluna 3 - Energia dissipada (Em[t=0] - Em[i])
            #coluna 4 - Energia dissipada [0,1] (Em[i]/Em[t=0])
        
        for i in range(len(v_v)):
            Em_v[i, 0] = ((massa*float(abs(v_v[i]))**2)/2)
            Em_v[i, 1] = massa*g*s_v[i]
            Em_v[i, 2] = float(Em_v[i,0]+Em_v[i,1])
            Em_v[i, 3] = (massa*g*h) - float(Em_v[i, 2])
            Em_v[i, 4] = Em_v[i, 2]/(massa*g*h)
        
        #12/09 - vmax precisa ser modificado
        vmax_v = max(abs(v_v))
        re_v, re24_v = reynolds(vmax_v, diametro)
        extra_v=array([['Vmax', vmax_v], ['Re', re_v], ['Re/24', re24_v]])
        data_array = vstack((data_array, extra_v))
        
        #Salva tabelas
        
        file_data=diretorio+'setup.csv'
        pd.DataFrame(data_array).to_csv(file_data, header=None, index=None)
        
        file_Em=diretorio+'em.csv'
        pd.DataFrame(Em_v).to_csv(file_Em, header=None, index=None)
        
        file_t=diretorio+'t.csv'
        pd.DataFrame(t_v).to_csv(file_t, header=None, index=None)
        
        file_v=diretorio+'v.csv'
        pd.DataFrame(v_v).to_csv(file_v, header=None, index=None)
        
        file_s=diretorio+'s.csv'
        pd.DataFrame(s_v).to_csv(file_s, header=None, index=None)
        
        file_f=diretorio+'f.csv'
        pd.DataFrame(f_v).to_csv(file_f, header=None, index=None)
        
        file_a=diretorio+'a.csv'
        pd.DataFrame(a_v).to_csv(file_a, header=None, index=None)
        
        return t_v, abs(v_v), s_v, f_v, a_v, Em_v, data_array
        
    if arrasto == 'both':
                
        t, v, s, f, a = calc(h, vinicial, diametro, massa, cd, 1, 1) #s, m/s, m, m/s2
        #Calcula arrasto de pressão
        
        Em = zeros([len(v), 5]) #J
        
        #Matriz EM:
            #coluna 0 - Energia Cinetica
            #coluna 1 - Energia potencial gravitacional
            #coluna 2 - Energia mecânica
            #coluna 3 - Energia dissipada (Em[t=0] - Em[i])
            #coluna 4 - Energia dissipada [0,1] (Em[i]/Em[t=0])
        
        for i in range(len(v)):
            Em[i, 0] = ((massa*float(abs(v[i]))**2)/2)
            Em[i, 1] = massa*g*s[i]
            Em[i, 2] = float(Em[i,0]+Em[i,1])
            Em[i, 3] = (massa*g*h) - float(Em[i, 2])
            Em[i, 4] = Em[i, 2]/(massa*g*h)
        
        #12/09 - vmax precisa ser modificado
        vmax = max(abs(v))
        re, re24 = reynolds(vmax, diametro)
        extra=array([['Vmax', vmax], ['Re', re], ['Re/24', re24]])
        data_array=vstack((data_array, extra))
        
        #Salva tabelas
        
        file_data=diretorio+'setup.csv'
        pd.DataFrame(data_array).to_csv(file_data, header=None, index=None)
        
        file_Em=diretorio+'em.csv'
        pd.DataFrame(Em).to_csv(file_Em, header=None, index=None)
        
        file_t=diretorio+'t.csv'
        pd.DataFrame(t).to_csv(file_t, header=None, index=None)
        
        file_v=diretorio+'v.csv'
        pd.DataFrame(v).to_csv(file_v, header=None, index=None)
        
        file_s=diretorio+'s.csv'
        pd.DataFrame(s).to_csv(file_s, header=None, index=None)
        
        file_f=diretorio+'f.csv'
        pd.DataFrame(f).to_csv(file_f, header=None, index=None)
        
        file_a=diretorio+'a.csv'
        pd.DataFrame(a).to_csv(file_a, header=None, index=None)
        
        return t, abs(v), s, f, a, Em, data_array
    
    if arrasto != "p" and arrasto!="v" and arrasto != "both":
        print("Arrasto inválido")

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print(current_time)
print("Iniciando simulação.")
#bolas=[['Futebol', 22.2, 454], ['Beisebol', 7.3, 145], ['Cricket', 7.2, 163], ['Basquete', 24.3, 600], ['Golfe', 4.3, 46], ['Tênis', 6.5, 58], ['Tênis de mesa', 3.8, 25], ['Voleibol', 21.0, 270], ['Wiffleball', 7.0, 145.3], ['Sepaktakraw', 13.7, 175]]
#bolas_arr=[['Futebol', 22.2, 454], ['Basquete', 24.3, 600], ['Tênis', 6.5, 58], ['Voleibol', 21.0, 270], ['Tênis de mesa', 3.8, 25]]
bolas_arr=[['Futebol', 22.2, 454]]
bolas_arr=array(bolas_arr)

h_tabela = arange(1, 101, 1) #m

#Tabela:
#0ª coluna: bola, string
#1ª coluna: diâmetro, cm
#2ª coluna: massa, g
#3ª coluna: velocidade terminal, m/s
#4ª coluna: velocidade máxima, m/s
#5ª coluna: altura mínima para atingir Vt, h
#6ª coluna: Re, adimensional

#tabela = [['Futebol', 22.2, 454, 0, 0, 0, 0], ['Basquete', 24.3, 600, 0, 0, 0, 0], ['Tênis', 6.5, 58, 0, 0, 0, 0], ['Voleibol', 21.0, 270, 0, 0, 0, 0], ['Tênis de mesa', 3.8, 25, 0, 0, 0, 0]]
tabela = [['Futebol', 22.2, 454, 0, 0, 0, 0]]
tabela = array(tabela)
#11/09 - Erro: coeficiente b tem valor diferente do esperado.

def alturamin(massag, diametrocm, vabs, s, i):
    global g, p, cd
    massa = massag/10**3
    raio = (diametrocm/10**2)/2
    A = (raio*raio)*pi
    coef_p = 0.5*p*cd*A
    vterminal = sqrt((2*massa*g)/coef_p)
    n=argmax(vabs >= vterminal)
    return vterminal, float(s[n])

raiz='C:/Users/breno/Documents/Drive - ifsp.edu.br/Estudo/PIC/11 CONICT/repo/data/'
if not os.path.exists(raiz):
    os.makedirs(raiz)
for k in range(len(h_tabela)):
    for x in range(len(bolas_arr)):
        t_a, v_a, s_a, f_a, a_a = calc(h_tabela[k], 0, float(bolas_arr[x, 1]), float(bolas_arr[x,2]), cd, 0, 1)
        v_a=abs(v_a)
        vmax=max(v_a)
        tabela[x, 1] = bolas_arr[x, 1]
        tabela[x, 2] = bolas_arr[x, 2]
        tabela[x, 3], tabela[x, 5] = alturamin(float(bolas_arr[x, 2]), float(bolas_arr[x, 1]), v_a, s_a, x)
        tabela[x, 4] = vmax

h = array([10, 50, 100])

for j in range(len(h)):
    for i in range(len(bolas_arr)):
        
        #plota para both (f5-f8)
        #diretorio='C:/Users/breno/Documents/Drive - ifsp.edu.br/Estudo/PIC/11 CONICT/repo/data/'+'both/'+str(h[j])+'/'+(bolas_arr[i, 0])+'/'
        #if not os.path.exists(diretorio):
            #os.makedirs(diretorio)
        #t, v, s, f, a, Em, data_array = simulacao(h[j], bolas_arr[i, 1], bolas_arr[i, 2], 0.45, 'both', bolas_arr[i, 0])
        #f5.plot(t, v, label=bolas_arr[i,0])
        #f6.plot(t, s, label=bolas_arr[i,0])
        #f7.plot(t, Em[:, 2], label=bolas_arr[i,0])
        #f8.plot(t, Em[:, 4], label=bolas_arr[i,0])
        ########################
        
        #plota para erro (f1-f4)
        #diretorio='C:/Users/breno/Documents/Drive - ifsp.edu.br/Estudo/PIC/11 CONICT/repo/data/'+'p/'+str(h[j])+'/'+(bolas_arr[i, 0])+'/'
        #if not os.path.exists(diretorio):
            #os.makedirs(diretorio)
        #t_p, v_p, s_p, f_p, a_p, Em_p, data_array_p = simulacao(h[j], bolas_arr[i, 1], bolas_arr[i, 2], 0.45, 'p', bolas_arr[i, 0])
        
        #inserir aqui: algoritmo 1 - para igualar os indices das matrizes
        
        ########################fim_algoritmo
        
        #v_erro = divide(v_p, v, out=zeros_like(v_p), where=v!=0)
        #s_erro = divide(s_p, s, out=zeros_like(s_p), where=s!=0)
        #f_erro = divide(f_p, f, out=zeros_like(f_p), where=f!=0)
        #a_erro = divide(a_p, a, out=zeros_like(a_p), where=a!=0)
        #Em_erro = divide(Em_p, Em, out=zeros_like(Em_p), where=Em!=0)
        
        #f1.plot(t_p, v_erro, label=bolas_arr[i,0])
        #f2.plot(t_p, s_erro, label=bolas_arr[i,0])
        #f3.plot(t_p, Em_erro[:, 2], label=bolas_arr[i,0])
        #f4.plot(t_p, Em_erro[:, 4], label=bolas_arr[i,0])
        ########################
        
        #plota para p (f13-f16)
        diretorio='C:/Users/breno/Documents/Drive - ifsp.edu.br/Estudo/PIC/11 CONICT/repo/data/'+'p/'+str(h[j])+'/'+(bolas_arr[i, 0])+'/'
        if not os.path.exists(diretorio):
            os.makedirs(diretorio)
        t_p, v_p, s_p, f_p, a_p, Em_p, data_array_p = simulacao(h[j], bolas_arr[i, 1], bolas_arr[i, 2], 0.45, 'p', bolas_arr[i, 0]) #unidades certas
        
        f13.plot(t_p, v_p, label=bolas_arr[i,0])
        f14.plot(t_p, s_p, label=bolas_arr[i,0])
        f15.plot(t_p, Em_p[:, 2], label=bolas_arr[i,0])
        f16.plot(t_p, Em_p[:, 4], label=bolas_arr[i,0])
        ########################
        
        #plota para v (f9-f12)
        #diretorio='C:/Users/breno/Documents/Drive - ifsp.edu.br/Estudo/PIC/11 CONICT/repo/data/'+'v/'+str(h[j])+'/'+(bolas_arr[i, 0])+'/'
        #if not os.path.exists(diretorio):
            #os.makedirs(diretorio)
        #t_v, v_v, s_v, f_v, a_v, Em_v, data_array_v = simulacao(h[j], bolas_arr[i, 1], bolas_arr[i, 2], 0.45, 'v', bolas_arr[i, 0])
        
        #f9.plot(t_v, v_v, label=bolas_arr[i,0])
        #f10.plot(t_v, s_v, label=bolas_arr[i,0])
        #f11.plot(t_v, Em_v[:, 2], label=bolas_arr[i,0])
        #f12.plot(t_v, Em_v[:, 4], label=bolas_arr[i,0])
        ########################
        
        #f1.grid()
        #f2.grid()
        #f3.grid()
        #f4.grid()
        
        #f5.grid()
        #f6.grid()
        #f7.grid()
        #f8.grid()
        
        #f9.grid()
        #f10.grid()
        #f11.grid()
        #f12.grid()
        
        f13.grid()
        f14.grid()
        f15.grid()
        f16.grid()
        
        #titulo erro (f1-f4)
        #f1.set_xlabel('Tempo (s)\nAltura: '+str(h[j])+'m\nErro (Arrasto cv²/bv + cv²)')
        #f2.set_xlabel('Tempo (s) \nAltura: '+str(h[j])+'m\nErro (Arrasto cv²/bv + cv²)')
        #f3.set_xlabel('Tempo (s) \nAltura: '+str(h[j])+'m\nErro (Arrasto cv²/bv + cv²)')
        #f4.set_xlabel('Tempo (s) \nAltura: '+str(h[j])+'m\nErro (Arrasto cv²/bv + cv²)')
        
        #f1.set_ylabel('Velocidade em módulo (m/s)')
        #f2.set_ylabel('Altura (m)')
        #f3.set_ylabel('Energia mecânica (J)')
        #f4.set_ylabel('Energia dissipada (Em/Em0)')
        #f4.set_ylim(-0.25, 1.25)
        
        #f1.legend(loc='upper left', bbox_to_anchor=(1, 1))
        #f2.legend(loc='upper left', bbox_to_anchor=(1, 1))
        #f3.legend(loc='upper left', bbox_to_anchor=(1, 1))
        #f4.legend(loc='upper left', bbox_to_anchor=(1, 1))    
        ######################

        #titulo both (f5-f8)
        #f5.set_xlabel('Tempo (s)\nAltura: '+str(h[j])+'m\nArrasto bv+cv²')
        #f6.set_xlabel('Tempo (s) \nAltura: '+str(h[j])+'m\nArrasto bv+cv²')
        #f7.set_xlabel('Tempo (s) \nAltura: '+str(h[j])+'m\nArrasto bv+cv²')
        #f8.set_xlabel('Tempo (s) \nAltura: '+str(h[j])+'m\nArrasto bv+cv²')
        
        #f5.set_ylabel('Velocidade em módulo (m/s)')
        #f6.set_ylabel('Altura (m)')
        #f7.set_ylabel('Energia mecânica (J)')
        #f8.set_ylabel('Energia dissipada (Em/Em0)')
        #f8.set_ylim(-0.25, 1.25)
        
        #f5.legend(loc='upper left', bbox_to_anchor=(1, 1))
        #f6.legend(loc='upper left', bbox_to_anchor=(1, 1))
        #f7.legend(loc='upper left', bbox_to_anchor=(1, 1))
        #f8.legend(loc='upper left', bbox_to_anchor=(1, 1))
        ######################
        
        #titulo v (f9-f12)
        #f9.set_xlabel('Tempo (s)\nAltura: '+str(h[j])+'m\nArrasto bv')
        #f10.set_xlabel('Tempo (s) \nAltura: '+str(h[j])+'m\nArrasto bv')
        #f11.set_xlabel('Tempo (s) \nAltura: '+str(h[j])+'m\nArrasto bv')
        #f12.set_xlabel('Tempo (s) \nAltura: '+str(h[j])+'m\nArrasto bv')
        
        #f9.set_ylabel('Velocidade em módulo (m/s)')
        #f10.set_ylabel('Altura (m)')
        #f11.set_ylabel('Energia mecânica (J)')
        #f12.set_ylabel('Energia dissipada (Em/Em0)')
        #f12.set_ylim(-0.25, 1.25)
        
        #f9.legend(loc='upper left', bbox_to_anchor=(1, 1))
        #f10.legend(loc='upper left', bbox_to_anchor=(1, 1))
        #f11.legend(loc='upper left', bbox_to_anchor=(1, 1))
        #f12.legend(loc='upper left', bbox_to_anchor=(1, 1))
        ######################
        
        #titulo p (f13-f16)
        f13.set_xlabel('Tempo (s)\nAltura: '+str(h[j])+'m\nArrasto cv²')
        f14.set_xlabel('Tempo (s) \nAltura: '+str(h[j])+'m\nArrasto cv²')
        f15.set_xlabel('Tempo (s) \nAltura: '+str(h[j])+'m\nArrasto cv²')
        f16.set_xlabel('Tempo (s) \nAltura: '+str(h[j])+'m\nArrasto cv²')
        
        f13.set_ylabel('Velocidade em módulo (m/s)')
        f14.set_ylabel('Altura (m)')
        f15.set_ylabel('Energia mecânica (J)')
        f16.set_ylabel('Energia dissipada (Em/Em0)')
        f16.set_ylim(-0.25, 1.25)
        
        f13.legend(loc='upper left', bbox_to_anchor=(1, 1))
        f14.legend(loc='upper left', bbox_to_anchor=(1, 1))
        f15.legend(loc='upper left', bbox_to_anchor=(1, 1))
        f16.legend(loc='upper left', bbox_to_anchor=(1, 1))
        ######################
    
    dirboth='C:/Users/breno/Documents/Drive - ifsp.edu.br/Estudo/PIC/11 CONICT/repo/data/'+'both/'+str(h[j])+'/'
    dirv='C:/Users/breno/Documents/Drive - ifsp.edu.br/Estudo/PIC/11 CONICT/repo/data/'+'v/'+str(h[j])+'/'
    dirp='C:/Users/breno/Documents/Drive - ifsp.edu.br/Estudo/PIC/11 CONICT/repo/data/'+'p/'+str(h[j])+'/'
    
    #salva grafico de erro 
    #vt_erro.savefig(dirboth+'vt_erro.svg', format='svg', dpi=1200, bbox_inches = 'tight', pad_inches = 0)
    #yt_erro.savefig(dirboth+'yt_erro.svg', format='svg', dpi=1200, bbox_inches = 'tight', pad_inches = 0)
    #em_erro.savefig(dirboth+'em_erro.svg', format='svg', dpi=1200, bbox_inches = 'tight', pad_inches = 0)
    #emd_erro.savefig(dirboth+'emd_erro.svg', format='svg', dpi=1200, bbox_inches = 'tight', pad_inches = 0)
    
    #salva grafico de both
    #vt_both.savefig(dirboth+'vt_both.svg', format='svg', dpi=1200, bbox_inches = 'tight', pad_inches = 0)
    #yt_both.savefig(dirboth+'yt_both.svg', format='svg', dpi=1200, bbox_inches = 'tight', pad_inches = 0)
    #em_both.savefig(dirboth+'em_both.svg', format='svg', dpi=1200, bbox_inches = 'tight', pad_inches = 0)
    #emd_both.savefig(dirboth+'emd_both.svg', format='svg', dpi=1200, bbox_inches = 'tight', pad_inches = 0)
    
    #salva grafico de v
    #vt_v.savefig(dirv+'vt_v.svg', format='svg', dpi=1200, bbox_inches = 'tight', pad_inches = 0)
    #yt_v.savefig(dirv+'yt_v.svg', format='svg', dpi=1200, bbox_inches = 'tight', pad_inches = 0)
    #em_v.savefig(dirv+'em_v.svg', format='svg', dpi=1200, bbox_inches = 'tight', pad_inches = 0)
    #emd_v.savefig(dirv+'emd_v.svg', format='svg', dpi=1200, bbox_inches = 'tight', pad_inches = 0)
    
    #salva grafico de p
    vt_p.savefig(dirp+'vt_p.svg', format='svg', dpi=1200, bbox_inches = 'tight', pad_inches = 0)
    yt_p.savefig(dirp+'yt_p.svg', format='svg', dpi=1200, bbox_inches = 'tight', pad_inches = 0)
    em_p.savefig(dirp+'em_p.svg', format='svg', dpi=1200, bbox_inches = 'tight', pad_inches = 0)
    emd_p.savefig(dirp+'emd_p.svg', format='svg', dpi=1200, bbox_inches = 'tight', pad_inches = 0)
    
    f1.cla()
    f2.cla()
    f3.cla()
    f4.cla()
    
    f5.cla()
    f6.cla()
    f7.cla()
    f8.cla()
    
    f9.cla()
    f10.cla()
    f11.cla()
    f12.cla()
    
    f13.cla()
    f14.cla()
    f15.cla()
    f16.cla()
    
print("Simulação concluída.")
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print(current_time)
    
#configure(1) #Ao invés de configurar, usa os dados do escopo do programa