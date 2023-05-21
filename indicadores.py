from dotenv import load_dotenv
from pathlib import Path
import os
import RPi.GPIO as GPIO
from time import sleep

dotenv_path = Path( './.env' )
load_dotenv( dotenv_path=dotenv_path )

class Indicadores:
    def __init__( self ):
        self.__PIN_LED_ROJO = int( os.getenv( 'PIN_LED_ROJO', 11 ))
        self.__PIN_LED_AMARILLO = int( os.getenv( 'PIN_LED_AMARILLO', 12 ) )
        self.__PIN_LED_VERDE = int( os.getenv( 'PIN_LED_VERDE', 13 ) )

        self.__PIN_BUZZER = int( os.getenv( 'PIN_BUZZER', 15 ) )
        self.__PIN_BOTON_CALIBRAR = int( os.getenv( 'PIN_BOTON_CALIBRAR', 16 ) )
        print( self.__PIN_LED_ROJO )

        GPIO.setwarnings( False )
        GPIO.setmode( GPIO.BOARD )
        self.__establecer_pines()

    def __establecer_pines ( self ):
        GPIO.setup( self.__PIN_LED_ROJO,     GPIO.OUT )
        GPIO.setup( self.__PIN_LED_AMARILLO, GPIO.OUT )
        GPIO.setup( self.__PIN_LED_VERDE,    GPIO.OUT )
        GPIO.setup( self.__PIN_BUZZER,       GPIO.OUT )

        GPIO.output( self.__PIN_LED_ROJO, GPIO.LOW )
        GPIO.output( self.__PIN_LED_AMARILLO, GPIO.LOW )
        GPIO.output( self.__PIN_LED_VERDE, GPIO.LOW )
        GPIO.output( self.__PIN_BUZZER, GPIO.LOW )

        GPIO.setup( self.__PIN_BOTON_CALIBRAR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN )

    def __encender_led ( self, pin ):
        GPIO.output( pin, GPIO.HIGH )
    def __apagar_led ( self, pin ):
        GPIO.output( pin, GPIO.LOW )

    def apagar_todo ( self ):
        self.__apagar_led( self.__PIN_LED_VERDE )
        self.__apagar_led( self.__PIN_LED_AMARILLO )
        self.__apagar_led( self.__PIN_LED_ROJO )
        self.__apagar_led( self.__PIN_BUZZER )

    def calibrado_correctamente ( self ):
        # Un pitido y un parpadeo del led verde por un segundo
        # Indica que el calibrado se realizo correctamente
        GPIO.output( self.__PIN_BUZZER, GPIO.HIGH )
        GPIO.output( self.__PIN_LED_VERDE, GPIO.HIGH )
        sleep( 1 )
        GPIO.output( self.__PIN_BUZZER, GPIO.LOW )
        GPIO.output( self.__PIN_LED_VERDE, GPIO.LOW )

    def no_se_detecto_rostro ( self ):
        # Se activa el led amarillo hasta que se detecte un rostro
        self.__apagar_led( self.__PIN_LED_VERDE )
        self.__apagar_led( self.__PIN_LED_ROJO )
        self.__encender_led( self.__PIN_LED_AMARILLO )


    def se_esta_detectando_rostro ( self ):
        # Apaga el led amarillo para indicar que se esta detectando un rostro
        self.__apagar_led( self.__PIN_LED_AMARILLO )

    def se_esta_detectando_somnoliencia ( self ):
        # Se activa el led rojo y el buzzer hasta que se deje de detectar somnoliencia
        self.__apagar_led( self.__PIN_LED_VERDE )
        self.__apagar_led( self.__PIN_LED_AMARILLO )
        self.__encender_led( self.__PIN_LED_ROJO )
        GPIO.output( self.__PIN_BUZZER, GPIO.HIGH )

    def no_se_detecto_somnoliencia ( self ):
        # Se apaga el led rojo y el buzzer en caso de que se haya detectado somnoliencia anteriormente
        self.__apagar_led( self.__PIN_LED_ROJO )
        GPIO.output( self.__PIN_BUZZER, GPIO.LOW )

    def no_se_detecto_rostro_en_calibrado ( self ):
        # Un pitido y un parpadeo del led rojo por un segundo
        # Indica que no se detecto un rostro en el calibrado
        GPIO.output( self.__PIN_BUZZER, GPIO.HIGH )
        GPIO.output( self.__PIN_LED_ROJO, GPIO.HIGH )
        sleep( 1 )
        GPIO.output( self.__PIN_BUZZER, GPIO.LOW )
        GPIO.output( self.__PIN_LED_ROJO, GPIO.LOW )

    def probar_buzzer ( self ):
        GPIO.output( self.__PIN_BUZZER, GPIO.HIGH )
        sleep( 1 )
        GPIO.output( self.__PIN_BUZZER, GPIO.LOW )
    
    def probar_leds ( self ):
        GPIO.output( self.__PIN_LED_ROJO, GPIO.HIGH )
        GPIO.output( self.__PIN_LED_AMARILLO, GPIO.HIGH )
        GPIO.output( self.__PIN_LED_VERDE, GPIO.HIGH )
        sleep( 1 )
        GPIO.output( self.__PIN_LED_ROJO, GPIO.LOW )
        GPIO.output( self.__PIN_LED_AMARILLO, GPIO.LOW )
        GPIO.output( self.__PIN_LED_VERDE, GPIO.LOW )

    def contador_con_leds ( self, tiempo: int ):
        self.__encender_led( self.__PIN_LED_ROJO )
        sleep( 1 )
        self.__apagar_led( self.__PIN_LED_ROJO )
        if tiempo == 1:
            return
        if tiempo == 2:
            self.__encender_led( self.__PIN_LED_VERDE )
            sleep( 1 )
            self.__apagar_led( self.__PIN_LED_VERDE )
            return
        for _ in range( tiempo - 2 ):
            self.__encender_led( self.__PIN_LED_AMARILLO )
            sleep( 1 )
            self.__apagar_led( self.__PIN_LED_AMARILLO )
            sleep( 0.3 )
        self.__encender_led( self.__PIN_LED_VERDE )
        sleep( 1 )
        self.__apagar_led( self.__PIN_LED_VERDE )


    def verificar_boton_calibrar ( self ):
        return GPIO.input( self.__PIN_BOTON_CALIBRAR ) == GPIO.HIGH


