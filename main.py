from threading import Timer
import cv2
import mediapipe as mp

from indicadores import Indicadores
from adminstrador_de_archivos import AdministradorDeArchivos
from verificaciones import obtener_distancias_entre_parpados, verificar_ojos_cerrados, verificar_somnoliencia

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

drawing_spec = mp_drawing.DrawingSpec( thickness=1, circle_radius=1 )
cap = cv2.VideoCapture( 0 )

face_mesh_options = {
    "max_num_faces": 1,
    "refine_landmarks": True,
    "min_detection_confidence": 0.5,
    "min_tracking_confidence": 0.5 
}

def main ():
    # Instacias de Classes
    # Clase que se encarga de el manejo del Rpi GPIO
    indicadores = Indicadores()
    # Clase que se encarga de el manejo de los archivos
    archivo = AdministradorDeArchivos()
    distancia_calibrado_ojo_derecho, distancia_calibrado_ojo_izquierdo = archivo.obtener_ultima_calibracion()
    cantidad_de_parapadeos = 0
    timerEstablecido = False
    with mp_face_mesh.FaceMesh( **face_mesh_options ) as face_mesh:
      while cap.isOpened():
        success, image = cap.read()
        if not success:
          print( "Ignoring empty camera frame." )
          continue

        image.flags.writeable = False
        image = cv2.cvtColor( image, cv2.COLOR_BGR2RGB )
        results = face_mesh.process( image )

        if indicadores.verificar_boton_calibrar(): # Pregunta si se presiono el boton de calibrar
            # Enciende los rojo, amarillo y verde por 1 segundo cada uno, y el amarillo parpadea 3 veces
            # para indicar que se esta calibrando
            indicadores.contador_con_leds( 5 ) 

            # Verifica que se haya detectado un rostro
            if results.multi_face_landmarks:
                indicadores.se_esta_detectando_rostro()
                captura_de_rostro = results.multi_face_landmarks[ 0 ]
                distancia_ojo_derecho, distancia_ojo_izquierdo = obtener_distancias_entre_parpados( captura_de_rostro )
                # Asignacion de las distancias calibradas
                distancia_calibrado_ojo_derecho = distancia_ojo_derecho
                distancia_calibrado_ojo_izquierdo = distancia_ojo_izquierdo
                print( 'Distancia ojo derecho calibrado: ', distancia_calibrado_ojo_derecho )
                print( 'Distancia ojo izquierdo calibrado: ', distancia_calibrado_ojo_izquierdo )

                # Grabar calibracion en archivo
                archivo.insertar_calibracion( distancia_calibrado_ojo_derecho, distancia_calibrado_ojo_izquierdo )
            else:
                print( 'No se detecto rostro en la calibracion' )
                indicadores.no_se_detecto_rostro_en_calibrado()
                    
        # Verifica la somnolencia
        if results.multi_face_landmarks:
            indicadores.se_esta_detectando_rostro()
            captura_de_rostro = results.multi_face_landmarks[ 0 ]
            ojo_derecho_cerrado, ojo_izquierdo_cerrado = verificar_ojos_cerrados( captura_de_rostro, distancia_calibrado_ojo_derecho, distancia_calibrado_ojo_izquierdo )
            cantidad_de_parapadeos += 1 if ojo_derecho_cerrado and ojo_izquierdo_cerrado else 0
            print( 'Ojo derecho cerrado: ', 'Si' if ojo_derecho_cerrado else 'No' )
            print( 'Ojo izquierdo cerrado: ', 'Si' if ojo_izquierdo_cerrado else 'No' )
            if not timerEstablecido:
                estaSomnoliento = Timer( 3, verificar_somnoliencia, [ cantidad_de_parapadeos, indicadores ] )
                estaSomnoliento.start()
                timerEstablecido = True

            else:
                cantidad_de_parapadeos = 0
                timerEstablecido = not timerEstablecido
        else:
            indicadores.no_se_detecto_rostro()
            
        image.flags.writeable = True
        image = cv2.cvtColor( image, cv2.COLOR_RGB2BGR )
        if results.multi_face_landmarks:
          indicadores.se_esta_detectando_rostro()
          for face_landmarks in results.multi_face_landmarks:
            mp_drawing.draw_landmarks( image=image, landmark_list=face_landmarks, connections=mp_face_mesh.FACEMESH_TESSELATION, landmark_drawing_spec=None, connection_drawing_spec=mp_drawing_styles .get_default_face_mesh_tesselation_style() )
            mp_drawing.draw_landmarks( image=image, landmark_list=face_landmarks, connections=mp_face_mesh.FACEMESH_CONTOURS, landmark_drawing_spec=None, connection_drawing_spec=mp_drawing_styles .get_default_face_mesh_contours_style() )
            mp_drawing.draw_landmarks( image=image, landmark_list=face_landmarks, connections=mp_face_mesh.FACEMESH_IRISES, landmark_drawing_spec=None, connection_drawing_spec=mp_drawing_styles .get_default_face_mesh_iris_connections_style() )
        else:
            indicadores.no_se_detecto_rostro()

        cv2.imshow( 'MediaPipe Face Mesh', cv2.flip( image, 1 ) )

        if cv2.waitKey( 5 ) & 0xFF == 27:
          break
    cap.release()   

if __name__ == "__main__":
    main()
