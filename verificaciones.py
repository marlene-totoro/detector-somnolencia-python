from threading import Timer

FACEMESH_PUNTOS_OJO_DERECHO = ( 159, 145 ) # 386 es el indice del punto de la parte superior del ojo derecho, y 374 es el indice del punto de la parte inferior del ojo derecho
FACEMESH_PUNTOS_OJO_IZQUIERDO = ( 386, 374 ) # 159 es el indice del punto de la parte superior del ojo izquierdo, y 145 es el indice del punto de la parte inferior del ojo izquierdo

def resetear_veces_que_se_ha_dormido ( detector_de_somnolencia ):
    detector_de_somnolencia[ 'veces_que_se_ha_dormido' ] = 0

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
    ojo_derecho_cerrado   = ( distancia_ojo_derecho < ( distancia_calibrado_ojo_derecho + ( distancia_calibrado_ojo_derecho * 0.005 ) ) )
    ojo_izquierdo_cerrado = ( distancia_ojo_izquierdo < ( distancia_calibrado_ojo_izquierdo +  ( distancia_calibrado_ojo_izquierdo * 0.005 ) ) )
    return ojo_derecho_cerrado, ojo_izquierdo_cerrado

def verificar_somnoliencia ( detector_de_somnolencia, indicadores ):
    # print( 'Cantidad de parpadeos: ', detector_de_somnolencia[ 'cantidad_de_parpadeos' ] )
    if detector_de_somnolencia[ 'cantidad_de_parpadeos' ] >= 84:
        print( 'Se detecto al conductor durmiendo con: ', detector_de_somnolencia[ 'cantidad_de_parpadeos' ] )
        indicadores.se_esta_detectando_somnoliencia()
        if not detector_de_somnolencia[ 'timer_veces_que_se_ha_dormido' ]:
            detector_de_somnolencia[ 'timer_veces_que_se_ha_dormido' ] = True
            estaSomnoliento = Timer( 600, resetear_veces_que_se_ha_dormido, [ detector_de_somnolencia ] )
            estaSomnoliento.start()
        detector_de_somnolencia[ 'veces_que_se_ha_dormido' ] += 1
        if detector_de_somnolencia[ 'veces_que_se_ha_dormido' ] >= 3:
            print( 'Se detecto al conductor durmiendo' )
            indicadores.se_realiza_frenado_de_emergencia()
    else:
        # print( 'No se detecto al conductor durmiendo' )
        indicadores.no_se_detecto_somnoliencia()
    detector_de_somnolencia[ 'cantidad_de_parpadeos' ] = 0
    detector_de_somnolencia[ 'timer' ] = False
