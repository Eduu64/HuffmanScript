# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 19:12:25 2024

@author: Eduardo
"""

import heapq
import math


class Nodo:
    def __init__(self, symbol=None, frequency=None):
        self.symbol = symbol
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency

def calcular_probabilidad_letras(texto):
    # Convertir el texto a minúsculas y filtrar solo letras
    texto_filtrado = [letra.lower() for letra in texto]
    # if letra.isalpha() para detectar solo letras del alfabeto
    
    # Contar el total de letras
    total_letras = len(texto_filtrado)
    
    # Crear un diccionario para contar las letras
    conteo_letras = {}
    for letra in texto_filtrado:
        if letra in conteo_letras:
            conteo_letras[letra] += 1
        else:
            conteo_letras[letra] = 1
    
    probabilidad_letras = [] 
    letras = []
    
    # Calcular la probabilidad de cada letra
    for letra, conteo in conteo_letras.items():
        letras.append(letra)  # Rellena con letras
        probabilidad_letras.append(conteo/total_letras)  # Rellena con frecuencias   
        
    return letras,probabilidad_letras

def arbolHuffman(arrayletras, arrayprobs):
    queue = [Nodo(letra, f) for letra, f in zip(arrayletras, arrayprobs)]
    heapq.heapify(queue)
    
    print("Formación del arbol:")
    
    while len(queue) > 1:
       print([(node.symbol, node.frequency) for node in queue])
       """
       Aquí, se extraen los dos nodos que tienen las frecuencias más bajas, 
       que se asignan a nodo_izq y nodo_der.
       """
       nodo_izq = heapq.heappop(queue)
       nodo_der = heapq.heappop(queue)
       """
       Se crea un nuevo nodo (merged_node) cuya frecuencia es la suma
       de las frecuencias de los dos nodos hijos que se acaban de extraer.
       """
       merged_node = Nodo(frequency = nodo_izq.frequency + nodo_der.frequency)
       """
       Se establece que el merged_node tiene como hijo izquierdo al nodo_izq 
       y como hijo derecho al nodo_der.
       """
       merged_node.left = nodo_izq
       merged_node.right = nodo_der
       
       """
       El nuevo nodo se inserta nuevamente en la queue.
       """
       heapq.heappush(queue, merged_node)
        
    return queue[0]

def codigoHuffman(node, code="",huffman_codes={}):
    if node is not None:
        if node.symbol is not None:
            huffman_codes[node.symbol] = code
            
        codigoHuffman(node.left, code + "0", huffman_codes)
        codigoHuffman(node.right, code + "1", huffman_codes)
        
        """
        nodos izq = codigo + 0
        nodos der = codigo + 1
        nodo = simbolo = codigo
        """
    
    return huffman_codes

def compresor(huffman_codes,texto):
    cadena_comprimida = ""
    for letra in texto:
        if(letra in huffman_codes):
            cadena_comprimida += huffman_codes[letra]
    return cadena_comprimida

def decompresor(huffman_codes, cadena_comprimida):
    cadena_decomprimida = ""
    codigo_actual = ""
    
    inverted_codes = {v: k for k, v in huffman_codes.items()}
    
    for bit in cadena_comprimida:
        codigo_actual += bit  # Agregar el bit actual al código acumulado
        
        # Si el código actual está en el diccionario invertido, agrega el símbolo correspondiente
        if codigo_actual in inverted_codes:
            cadena_decomprimida += inverted_codes[codigo_actual]  # Agregar símbolo a la cadena
            codigo_actual = ""  # Reiniciar el código acumulado

    return cadena_decomprimida

def calculo_entropia(probabilidad_letras):
    entropia = sum(x*math.log((1/x), 2.0) for x in probabilidad_letras)
    return entropia

def longitud_media(texto,compreso):
    #print(len(compreso))
    #print(len(texto))
    longitud_media = len(compreso)/len(texto)
    return longitud_media



texto = "aaaabbcd"
arrayletras, arrayprobs = calcular_probabilidad_letras(texto)
print(arrayletras,arrayprobs)
print(" ")
#arrayletras = ['a', 'b', 'c', 'd']
#arrayprobs = [0.5, 0.25, 0.125, 0.125]
arbol = arbolHuffman(arrayletras, arrayprobs)
huffman_codes = codigoHuffman(arbol)
print(" ")
for char, code in huffman_codes.items():
    print(f"Letra: {char} Bits: {code}")
compreso = compresor(huffman_codes,texto)
print("")
print(f"Comprimido: {compreso}")
entropia = calculo_entropia(arrayprobs)
decompreso = decompresor(huffman_codes,compreso)
print("")
print(f"Descomprimido: {decompreso}")
print("")
print(f"Entropía: {entropia} bits/simbolo")
longitudmedia = longitud_media(texto,compreso)
print("")
print(f"longitud media: {longitudmedia} bits")

