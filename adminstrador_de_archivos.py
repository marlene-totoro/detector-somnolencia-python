import os
from dotenv import load_dotenv
from pathlib import Path
dotenv_path = Path( './.env' )
load_dotenv( dotenv_path=dotenv_path )

class AdministradorDeArchivos:
    def __init__( self ):
        self.__NOMBRE_ARCHIVO_CALIBRACION = os.getenv( 'NOMBRE_ARCHIVO_CALIBRACION', 'nocali' )
        self.__RUTA_ARCHIVO_CALIBRACION = os.getenv( 'RUTA_ARCHIVO_CALIBRACION', './' )
        self.__ARCHIVO = f"{ self.__RUTA_ARCHIVO_CALIBRACION }/{ self.__NOMBRE_ARCHIVO_CALIBRACION }.txt"
        self.__crear_archivo_si_no_existe()

    def __crear_archivo_si_no_existe ( self ):
        archivo = open( self.__ARCHIVO, "a" )
        archivo.close()

    def insertar_calibracion ( self, distancia_calibrado_ojo_derecho, distancia_calibrado_ojo_izquierdo ):
        archivo = open( self.__ARCHIVO, "a" )
        archivo.write( f"{ distancia_calibrado_ojo_derecho },{ distancia_calibrado_ojo_izquierdo }\n" )
        archivo.close()

    def obtener_ultima_calibracion ( self ):
        try:
            archivo = open( self.__ARCHIVO, "r" )
            contenido = archivo.readlines()
            archivo.close()
            ultima_linea = contenido[ -1 ]
            if len( ultima_linea ) == 0:
                return 0, 0
            ultima_calibracion = ultima_linea.split( "," )
            distancia_calibrado_ojo_derecho = float( ultima_calibracion[ 0 ] )
            distancia_calibrado_ojo_izquierdo = float( ultima_calibracion[ 1 ] )
            return distancia_calibrado_ojo_derecho, distancia_calibrado_ojo_izquierdo
        except:
            return 0, 0
