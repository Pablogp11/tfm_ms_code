# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 12:28:52 2024

@author: usuario
"""

"Creamos un diccionario con los items que vamos a pasar por la request a la API"

import numpy as np
import openai
import os
import pandas as pd
import time
import pathlib 

"Creamos una carpeta que se llma tfm_ms con un directorio hijo data donde se van a volcar los resultados. \
"

def crear_directorio(directorio) : #Definimos el entorno donde se van a guardar los datos
    if not os.path.exists(directorio) and directorio not in str(pathlib.Path().absolute()).replace("\\","/") :
        return os.makedirs(directorio)
        print(f'Se ha creado el directorio {directorio} a las {time.strftime("%d/%m/%y")}')
    else:
        pass
        print('Ya existe el directorio donde se van a cargar los datos')
    try:
        os.chdir(directorio) #Cambiar de directorio al que se acaba de crear
    except:
         pass
     
       
crear_directorio('data')

head_question = "Recrea una llamada de un call center de energía donde el tema de conversación sea "

lista_items = ["descontento con la factura porque el coste de este mes es mucho mayor al del anterior o porque el coste es mayor al que se esperaba con tono enfadado por parte del cliente, puedes incluir datos númericos en euros por parte del cliente",
               "no se comprende alguno o algunos de los siguientes conceptos de la factura: potencia contrada, el consumo en cada tramo horario,  facturación por potencia contratada, peajes y cargos, impuesto sobre la electricidad y el IVA. El cliente puede preguntar por uno o por varios de estos conceptos",
               "ha habido un cambio en las condiciones de contrato y el cliente ha recibido un mensaje en el que se le pide que las acepte, el cliente quiere saber como hacer esto, el tono de la conversación es neutro, es una conversación a modo informativa",
               "pregunta acerca de los formatos de las facturas, la conversación sigue un tono neutro",
               "el cliente quiere cambiar su tipo de tarifa, actualmente tiene contratada una tarifa estable de precio fijo y quiere cambiar a una tarifa del mercado regulado",
               "el cliente ha notado que alguno de sus datos personales no es correcto y quiere cambiarlo, los datos personales son los siguientes: Nombre,apellidos,codigo postal,calle y DNI",
               "el cliente pide información acerca de los distintos tipos de tarifas que puede contratar, estas son: tarifa del mercado regulado y tarifa del mercado libre. El cliente puede preguntar por una o por las dos, si pregunta por las dos el agente debe explicarle las principales diferencias , la conversacion debe seguir un tono neutro",
               "pregunta del cliente acerca del ciclo de facturación y acerca de como puede cambiarlo",
               "descontento del cliente porque no entiende porque le ha subido tanto la factura, la conversación debe seguir un tono neutro, el agente debe explicar que su factura ha subido debido a la subida del IVA por parte del gobierno que entraba en vigor el 1 de Enero de 2024",
               "descontento del cliente porque no entiende porque le ha subido tanto la factura, la conversación debe seguir un tono neutro, el agente debe explicar que una posible causa del incremento de su factura es haber consumido más energía o haber utilizado más energía en un tramo donde la luz es más costosa",
               "el cliente esta interesado en saber por qué la luz es más cara a unas horas que a otras. La llamada sigue un tono neutro",
               "el cliente llama para quejarse de una avería en la red y el agente que responde le informa que las averías en la red deben ser comunicadas a la empresa distribuidora no a la comercializadora. El agente le proporciona el numero de atención al cliente de la distribuidora",
               "el cliente quiere información acerca de las diferentes formas de pago y plazos de su factura. El plazo para pagar la factura es de 20 días antes de que se corte el suministro. El agente debe explicarle que existen 4 formas de pago: Domiciliación bancaria, pago por telefono, pago online o pago en efectivo en una sucursal bancaria.",
               "el cliente ha observado un incremento en su factura de la luz y le gustaría obtener información acerca de como mejorar la eficiencia energética para pagar menos"]

lista_items_with_header = [head_question + iteracion for iteracion in lista_items]

number_items = list(range(len(lista_items)))

diccionario_items = dict(zip(number_items,lista_items_with_header))

"Se define la función que va a lanzar la request a la API "

openai.api_key = 'Insertar API Key'

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.8,
        presence_penalty = 0.5
    )
    return response.choices[0].message["content"]

"Para automatizar y ganar riqueza en la creación del set de datos se va a elegir de forma aleatoria el tema de conversación que se va a generar.\
    Además, para adecuarnos a la limitaciones de la propia API de OpenAI se lanzan las peticiones en un batch de 200"


number_request = 1000 #Número de llamadas que se van a ahacer sobre la API


df_raw = pd.DataFrame(columns=['motivo_llamada','id_llamada','llamada_registro'],index = range(number_request)) #Crear el dataset estructurado sobre el que se van a volcar los registros de las llamadas

time_clock = time.strftime("%d/%m/%y")
time_clock = time_clock.replace('/', '_')
text_file = 'historic_request_' + time_clock

file = open(text_file,"w") #Crear un log histórico  de las peticiones que se lanzan

for request_iter in range(0,number_request):
    random_number = np.random.randint(0, high=len(lista_items), dtype=int) #Componente aleatorio que accede al diccionario de items
    
    print(f' Se ha generado la iteración {request_iter} sobre el tema {random_number} \n')

    
    prompt = diccionario_items[random_number]
    
    print(prompt + '\n')
    file.write(prompt + os.linesep)
    
    respuesta = get_completion(prompt)
    df_raw.iloc[request_iter,0] = prompt
    df_raw.iloc[request_iter,1] = random_number
    df_raw.iloc[request_iter,2] = respuesta
    
    time.sleep(2)
    #print(respuesta)
    time.sleep(5)

file.close()

# Escribir el dataframe en excel 

excel_file = "data_call_raw_" + time_clock + ".xlsx"

df_raw.to_excel(excel_file,
                index=True)