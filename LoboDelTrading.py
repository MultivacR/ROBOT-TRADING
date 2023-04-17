# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 11:25:09 2023

@author: DAVID ERNESTO RAMIREZ ARBOLEDA
"""


import ctypes
import time 
import os
import datetime
import math
from binance.client import Client

def acceder(espera=1):
    diccionario={"secretKey":"YOUR SECRET KEY",
                  "apiKey":"YOUR API KEY",
                  "symbol":"BTCTUSD"}
    while True:
        try: 
            client = Client(diccionario["apiKey"],diccionario["secretKey"])
            print("Ingreso Exitoso**") 
            print(datetime.datetime.now())
            return(client)
        except:
            print("str(NameError)")  
            time.sleep(espera)
            
api_key = 'API KEY'
secret_key = 'SECRET KEY'


# Conectar a la API de Binance
client = Client(api_key, secret_key)

def ObtenerSaldo(moneda): #ejemplo"BTC"
    explorar = client.get_margin_account()['userAssets']
    balance=0
    for x in explorar:
       if x["asset"]==moneda:
           balance=float(x["free"])
           break
    print("Balance=",balance,moneda)
    return(balance)

def vender2terciosBtc(symbol):
    try:
       balance=ObtenerSaldo("BTC")
       print(balance)
       if balance <= 0:
           print('No hay saldo disponible de BTC en margen cruzado')
           return False
       order = client.create_margin_order(
           symbol=symbol,
           side=Client.SIDE_SELL,
           type=Client.ORDER_TYPE_MARKET,
           quantity=round(balance*0.7,5), #NO PERMITE VENDER EL 100% DEL SALDO. Cabrones!!!
           )
       print(f'Orden de venta de {balance:.6f} BTC colocada exitosamente')
       return order
    except:
       return(False)
   
def vender_todo_btc_market(symbol):
    try:
       balance=ObtenerSaldo("BTC")
       print(balance)
       if balance <= 0:
           print('No hay saldo disponible de BTC en margen cruzado')
           return False
       order = client.create_margin_order(
           symbol=symbol,
           side=Client.SIDE_SELL,
           type=Client.ORDER_TYPE_MARKET,
           quantity=round(balance*0.99,5), #NO PERMITE VENDER EL 100% DEL SALDO. Cabrones!!!
           )
       print(f'Orden de venta de {balance:.6f} BTC colocada exitosamente')
       return order
    except:
       return(False)
   
def comprar2terciosbtc(symbol): #porqueria de función está replicando codigo anterior
    try:
        # Obtener el balance disponible de TUSD en la cuenta de margen cruzado
        explorar = client.get_margin_account()['userAssets']
        for x in explorar:
            if x["asset"]=="TUSD":
                TUSD_balance=float(x["free"])
    #TUSD_balance = float(client.get_margin_account()['totalNetAssetOfTUSD'])
        print(TUSD_balance,"TUSD BALANCE")
    # Obtener el último precio de BTC
        ticker = client.get_symbol_ticker(symbol=symbol)
        last_price = float(ticker['price'])    
    # Calcular la cantidad de BTC que se puede comprar con el balance de TUSD
        quantity = round((TUSD_balance / last_price)*0.7,5) 
        print(quantity,"$$$$$$$$$$$$$$")
    # Colocar la orden de compra de mercado
        order = client.create_margin_order(
            symbol=symbol,
            side=Client.SIDE_BUY,
            type=Client.ORDER_TYPE_MARKET,
            quantity=quantity
            )
        print(f'Orden de compra de {quantity:.6f} BTC a mercado colocada exitosamente')
        print(order)
        return order
    except ValueError as error:
            print(x,error)
            
def comprar_btc_con_TUSD_orden_de_mercado(symbol): #dejar ese 0.98 quieto!!!!
    try:
        # Obtener el balance disponible de TUSD en la cuenta de margen cruzado
        explorar = client.get_margin_account()['userAssets']
        for x in explorar:
            if x["asset"]=="TUSD":
                TUSD_balance=float(x["free"])
    #TUSD_balance = float(client.get_margin_account()['totalNetAssetOfTUSD'])
        print(TUSD_balance,"TUSD BALANCE")
    # Obtener el último precio de BTC
        ticker = client.get_symbol_ticker(symbol=symbol)
        last_price = float(ticker['price'])    
    # Calcular la cantidad de BTC que se puede comprar con el balance de TUSD
        quantity = round((TUSD_balance / last_price)*0.98,5) #NO MOVER!!! DEJAR QUIETO!!!!
        print(quantity,"$$$$$$$$$$$$$$")
    # Colocar la orden de compra de mercado
        order = client.create_margin_order(
            symbol=symbol,
            side=Client.SIDE_BUY,
            type=Client.ORDER_TYPE_MARKET,
            quantity=quantity
            )
        print(f'Orden de compra de {quantity:.6f} BTC a mercado colocada exitosamente')
        return order
    except ValueError as error:
            print(x,error)
            
def esperar(hasta=59): #operamos a los 59:52 mins por si tiene que intentar comprar o vender varias veces
    log("*********************")    
    hora_actual = datetime.datetime.now().time()
    if hora_actual.minute*60+hora_actual.second<hasta*60:
        print("Dentro")
        time.sleep(hasta*60-hora_actual.minute*60-hora_actual.second+52)
    log(datetime.datetime.now().time())
    
def log(palabra):
    palabra=str(palabra)
    with open("log.txt", "a") as file:
        current_time = time.strftime("%D:%H:%M:%S")
        file.write(current_time +palabra+ "\n")
        print(f"Hora actual: {current_time}","   ", palabra)
        
def logbalances(a,b):
    ticker=0
    try:
        ticker = client.get_ticker(symbol='BTCTUSD') 
    except :
        pass
    current_time = time.strftime("%D:%H:%M:%S")    
    with open("logbalances.txt", "a") as file:
        file.write("\n"+str(current_time)+"  \t"+str(a)+"  \t"+str(b)+"  \t"+str(ticker['lastPrice']))
        

def logcorto():
    ticker=0
    try:
        ticker = client.get_ticker(symbol='BTCTUSD') 
        current_time = time.strftime("%D:%H:%M:%S")
        a=ObtenerSaldo("TUSD")
    except :
        pass   
    with open("logcorto.txt", "a") as file:
        file.write("\n"+str(current_time)+"  \t"+str(a)+"  \t"+str(ticker['lastPrice']))
        
def loglargo():
    ticker=0
    try:
        ticker = client.get_ticker(symbol='BTCTUSD') 
        current_time = time.strftime("%D:%H:%M:%S")
        a=ObtenerSaldo("BTC")
    except :
        pass   
    with open("loglargo.txt", "a") as file:
        file.write("\n"+str(current_time)+"  \t"+str(a)+"  \t"+str(ticker['lastPrice']))

def CrearData0(k): #recibo las tres ultimas velas, voy a trabajar con la ULTIMA Y PENULTIMA (actual y anterior)
    velas=k.get_klines(symbol='BTCTUSD', interval=Client.KLINE_INTERVAL_1HOUR,limit=4) # Ultimas tres horas
    tiempo=datetime.datetime.now().time().second
    factor=(3540+tiempo)/3600
    a=float(velas[3][4])-float(velas[3][1]) #ultimo cambio precio
    b=float(velas[3][5])-float(velas[2][5]) #ultimo cambio volumen
    c=float(velas[2][4])-float(velas[2][1])  #cambio precios hace una vela
    d=float(velas[2][5])-float(velas[1][5])   #cambio de volumen 2 periodos
    #print("\n**\n",velas[2][1],velas[1][1],velas[2][5],velas[1][5],velas[1][1],velas[0][1],velas[1][5],velas[0][5])
    x=[a,b,c,d]
    print(x)
    r=""
    for y in x:
        if y>0:
            r=r+"1"
        else:
            r=r+"0" 
    log("data")
    log(r)
    return(r)

def politica(data): #1=Comprar 0=Vender la usamos para velas de horas.
    dataInt=int(data, 2) ## (ultima vela 1 sube 0 baja)(ultimo vol)(penultima vel )(penultimo vol)
    alza=[0,1,2,3,8,12,13,15]
    baja=[4,5,6,7,9,10,11,14]
    #=IF(OR(G3=0;G3=1;G3=2;G3=3;G3=8;G3=12;G3=13;G3=15);(A4-A3)/A3;-(A4-A3)/A3)
    print(dataInt)
    print("alza=[0,1,2,3,4,6,8,9,12,13,15]   baja=[5,7,10,11,13,14]")
    print("nueva alza [0,1,2,3,8,12,13,15] nueva baja [4,5,6,7,9,10,11,14]")
    log(dataInt)
    if dataInt in alza:
        log("politica retorna comprar")
        return("comprar")
    if dataInt in baja:
        log("politica retorna vender")
        return("vender")
        
       
def operar(hacer,a):
    log("ingreso en operar")
    d="Error por defecto"
    try:
        btc_balance,TUSD_balance,ticker = ObtenerSaldo("BTC"),ObtenerSaldo("TUSD"),float(a.get_ticker(symbol='BTCTUSD')['lastPrice']) 
        btc_balance_in_dolar=btc_balance*ticker        
        if btc_balance_in_dolar-TUSD_balance>0 and hacer=="comprar":
            log("SOSTENER OPERACION----largo ")
            largo(True)
            return(True)
        if  TUSD_balance-btc_balance_in_dolar>0 and hacer=="vender":
            log("repetir corto----corto ")
            corto(True)
            return(True)
            
    except ValueError as error:
        log("error en operar, primera parte")
        log(error)
        
    if hacer=="comprar":
        largo(False)
    if hacer=="vender":
        corto(False) 

            
def CerrarSaldos():
    log("cerrar Saldos")
    k=ObtenerSaldo("TUSD")
    r=ObtenerSaldo("BTC")
    m=False
    try:
        transaction = client.repay_margin_loan(asset='TUSD', amount=str(k))
        transaction = client.repay_margin_loan(asset='TUSD', amount=str(r*0.2))
    except:
        pass        
    
    try:
        transaction = client.repay_margin_loan(asset='BTC', amount=str(r))
        transaction = client.repay_margin_loan(asset='BTC', amount=str(r*0.2))
    except:        
        pass  
    log("finalizado cerrar saldos")
    return(True)


def buscar(activo):
    r=client.get_margin_account()
    i=0
    for x in r['userAssets']:
        if x["asset"]==activo:
            return(i)
        i+=1
    return(False)
    

def corto(sostener):
    
    log("cortoInit")
    if sostener==False:
        try:
            vender_todo_btc_market('BTCTUSD')
        except ValueError as error:
            log("error a en primer try del corto")
            log(error)
    
    else:
        try:
            comprar2terciosbtc('BTCTUSD')
        except:
            pass
    time.sleep(1)
    CerrarSaldos()
    while datetime.datetime.now().time().minute>55:
        time.sleep(0.1)
    time.sleep(1)
    try:
        max_loan = round(float(client.get_max_margin_loan(asset='BTC')["amount"])-0.00001,5)
        transaction = client.create_margin_loan(asset='BTC',amount=str(max_loan))
        log("apalancamiento en corto exitoso")
    except ValueError as error:
        log("error al apalancar en corto")
        log(error)
    try:            
        vender_todo_btc_market('BTCTUSD')
        log("cortoend")
    except:
        log("error al vender btc con orden de mercado")
    max_loan=None
    logcorto()

def largo(sostener):
    log("largoInit")
    if sostener==False:
        try:
            comprar_btc_con_TUSD_orden_de_mercado('BTCTUSD')
        except ValueError as error:
            log("error al comprar btc ")
            log(error)
    else:
        try:
            vender2terciosBtc('BTCTUSD')
        except:
            pass
    time.sleep(1)
    CerrarSaldos()  
    
    while datetime.datetime.now().time().minute>55:        
        time.sleep(0.1)
    time.sleep(1)
    try:    
           ##reparacion  APIError(code=-3045): The system does not have enough asset now.
        max_loan = round(float(client.get_max_margin_loan(asset='TUSD')["amount"])-0.01,2)
        transaction = client.create_margin_loan(asset='TUSD',amount=str(max_loan))
        log("apalancamiento en largo exitoso")
    except  ValueError as error:
        log("error al apalancar en largo")
        log(error)
    try:
        comprar_btc_con_TUSD_orden_de_mercado('BTCTUSD')
        log("largoend")
    except:
        log("error al comprar btc con orden de mercado")
    max_loan=None
    loglargo()


while(True):
    print("*")    
    while(datetime.datetime.now().time().minute<58):
        time.sleep(30)
    log("salió de esperar")
    esperar()
    k=acceder()
    s=CrearData0(k)
    r=politica(s)
    if datetime.datetime.now().time().minute<5:
        log("NO SE PUDO OPERAR SE PASÓ DEL TIEMPO")
    elif datetime.datetime.now().time().minute==59:
        try:
            operar(r,k)
            #time.sleep(20)
        except ValueError as error:
            log("error en operar linea 324"+str(error))
    try:
        log(ObtenerSaldo("TUSD"))
        log(ObtenerSaldo("BTC"))
        logbalances(ObtenerSaldo("TUSD"),ObtenerSaldo("BTC"))
    except:
        log("error 00052")
    ctypes.windll.PowrProf.SetSuspendState(0, 1, 0)
    #time.sleep(300)
    
"""
##corto

comprar2terciosbtc('BTCTUSD')
time.sleep(1)
CerrarSaldos()
##largo

vender2terciosBtc('BTCTUSD')
time.sleep(1)
CerrarSaldos()  """
#inspect.currentframe() con import inspect se uspone que imprime la linea de ejecucion