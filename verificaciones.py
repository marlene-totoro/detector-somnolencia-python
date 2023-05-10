FACEMESH_PUNTOS_OJO_DERECHO = ( 159, 145 ) # 386 es el indice del punto de la parte superior del ojo derecho, y 374 es el indice del punto de la parte inferior del ojo derecho
FACEMESH_PUNTOS_OJO_IZQUIERDO = ( 386, 374 ) # 159 es el indice del punto de la parte superior del ojo izquierdo, y 145 es el indice del punto de la parte inferior del ojo izquierdo

def obtener_distancias_entre_parpados( captura_de_rostro ):
    # Obtencion de las coordenadas de los puntos de interes
    coordenadas_punto_sup_ojo_derecho = captura_de_rostro.landmark[ FACEMESH_PUNTOS_OJO_DERECHO[ 0 ] ]
    coordenadas_punto_inf_ojo_derecho = captura_de_rostro.landmark[ FACEMESH_PUNTOS_OJO_DERECHO[ 1 ] ]
    coordenadas_punto_sup_ojo_izquierdo = captura_de_rostro.landmark[ FACEMESH_PUNTOS_OJO_IZQUIERDO[ 0 ] ]
    coordenadas_punto_inf_ojo_izquierdo = captura_de_rostro.landmark[ FACEMESH_PUNTOS_OJO_IZQUIERDO[ 1 ] ]

    # Calculo de la distancia entre los puntos de interes usando la distancia euclidiana( Pitagoras )
    distancia_ojo_derecho = ( ( coordenadas_punto_sup_ojo_derecho.x - coordenadas_punto_inf_ojo_derecho.x ) ** 2 + ( coordenadas_punto_sup_ojo_derecho.y - coordenadas_punto_inf_ojo_derecho.y ) ** 2 ) ** 0.5
    distancia_ojo_izquierdo = ( ( coordenadas_punto_sup_ojo_izquierdo.x - coordenadas_punto_inf_ojo_izquierdo.x ) ** 2 + ( coordenadas_punto_sup_ojo_izquierdo.y - coordenadas_punto_inf_ojo_izquierdo.y ) ** 2 ) ** 0.5
    return distancia_ojo_derecho, distancia_ojo_izquierdo

def verificar_ojos_cerrados ( captura_de_rostro, distancia_calibrado_ojo_derecho, distancia_calibrado_ojo_izquierdo ):
    distancia_ojo_derecho, distancia_ojo_izquierdo = obtener_distancias_entre_parpados( captura_de_rostro )
    ojo_derecho_cerrado   = ( distancia_ojo_derecho < ( distancia_calibrado_ojo_derecho * 0.6 ) )
    ojo_izquierdo_cerrado = ( distancia_ojo_izquierdo < ( distancia_calibrado_ojo_izquierdo * 0.6 ) )
    return ojo_derecho_cerrado, ojo_izquierdo_cerrado

def verificar_somnoliencia ( cantidad_de_parapadeos ):
    return cantidad_de_parapadeos >= 100


