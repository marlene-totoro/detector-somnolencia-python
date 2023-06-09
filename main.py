import sys
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
    detector_de_somnolencia = {
        'timer': False,
        'cantidad_de_parpadeos': 0,
        'veces_que_se_ha_dormido': 0,
        'timer_veces_que_se_ha_dormido': False,
    }
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
            print( 'se realizara la calibracion' )
            indicadores.contador_con_leds( 5 ) 
            

            # Verifica que se haya detectado un rostro
            if results.multi_face_landmarks:
                indicadores.se_esta_detectando_rostro()
                captura_de_rostro = results.multi_face_landmarks[ 0 ]
                distancia_ojo_derecho, distancia_ojo_izquierdo = obtener_distancias_entre_parpados( captura_de_rostro )
                # Asignacion de las distancias calibradas
                distancia_calibrado_ojo_derecho = distancia_ojo_derecho
                distancia_calibrado_ojo_izquierdo = distancia_ojo_izquierdo
                #print( 'Distancia ojo derecho calibrado: ', distancia_calibrado_ojo_derecho )
                #print( 'Distancia ojo izquierdo calibrado: ', distancia_calibrado_ojo_izquierdo )

                # Grabar calibracion en archivo
                archivo.insertar_calibracion( distancia_calibrado_ojo_derecho, distancia_calibrado_ojo_izquierdo )
                indicadores.calibrado_correctamente()
            else:
                print( 'No se detecto rostro en la calibracion' )
                indicadores.no_se_detecto_rostro_en_calibrado()
                    
        # Verifica la somnolencia
        if results.multi_face_landmarks:
            indicadores.se_esta_detectando_rostro()
            captura_de_rostro = results.multi_face_landmarks[ 0 ]
            ojo_derecho_cerrado, ojo_izquierdo_cerrado = verificar_ojos_cerrados( captura_de_rostro, distancia_calibrado_ojo_derecho, distancia_calibrado_ojo_izquierdo )
            detector_de_somnolencia[ 'cantidad_de_parpadeos' ] += 1 if ojo_derecho_cerrado and ojo_izquierdo_cerrado else 0
            # print( 'Ojo derecho cerrado: ', 'Si' if ojo_derecho_cerrado else 'No' )
            # print( 'Ojo izquierdo cerrado: ', 'Si' if ojo_izquierdo_cerrado else 'No' )
            # print( 'Cantidad de parpadeos: ', detector_de_somnolencia[ 'cantidad_de_parpadeos' ] )
            if not detector_de_somnolencia[ 'timer' ]:
                detector_de_somnolencia[ 'timer' ] = True
                estaSomnoliento = Timer( 5, verificar_somnoliencia, [ detector_de_somnolencia, indicadores ] )
                estaSomnoliento.start()
        else:
            indicadores.no_se_detecto_rostro()
            
        image.flags.writeable = True
        image = cv2.cvtColor( image, cv2.COLOR_RGB2BGR )
        if results.multi_face_landmarks:
          indicadores.se_esta_detectando_rostro()
          for face_landmarks in results.multi_face_landmarks:
            # mp_drawing.draw_landmarks( image=image, landmark_list=face_landmarks, connections=mp_face_mesh.FACEMESH_TESSELATION, landmark_drawing_spec=None, connection_drawing_spec=mp_drawing_styles .get_default_face_mesh_tesselation_style() )
            mp_drawing.draw_landmarks( image=image, landmark_list=face_landmarks, connections=mp_face_mesh.FACEMESH_LEFT_EYE, landmark_drawing_spec=None, connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style() )
            mp_drawing.draw_landmarks( image=image, landmark_list=face_landmarks, connections=mp_face_mesh.FACEMESH_RIGHT_EYE, landmark_drawing_spec=None, connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style() )
            # mp_drawing.draw_landmarks( image=image, landmark_list=face_landmarks, connections=mp_face_mesh.FACEMESH_IRISES, landmark_drawing_spec=None, connection_drawing_spec=mp_drawing_styles .get_default_face_mesh_iris_connections_style() )
        else:
            indicadores.no_se_detecto_rostro()

        cv2.imshow( 'MediaPipe Face Mesh', cv2.flip( image, 1 ) )

        if cv2.waitKey( 5 ) & 0xFF == 27:
          indicadores.apagar_todo()
          sys.exit()
          break
    cap.release()   

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        indicadores.apagar_todo()
        sys.exit()
