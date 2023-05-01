import cv2
import mediapipe as mp

from indicadores import Indicadores
from adminstrador_de_archivos import AdministradorDeArchivos

FACEMESH_PUNTOS_OJO_DERECHO = ( 159, 145 ) # 386 es el indice del punto de la parte superior del ojo derecho, y 374 es el indice del punto de la parte inferior del ojo derecho
FACEMESH_PUNTOS_OJO_IZQUIERDO = ( 386, 374 ) # 159 es el indice del punto de la parte superior del ojo izquierdo, y 145 es el indice del punto de la parte inferior del ojo izquierdo

# Classes
# Clase que se encarga de el manejo del Rpi GPIO
indicadores = Indicadores()

# Clase que se encarga de el manejo de los archivos
archivo = AdministradorDeArchivos()

distancia_calibrado_ojo_derecho, distancia_calibrado_ojo_izquierdo = archivo.obtener_ultima_calibracion()

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

drawing_spec = mp_drawing.DrawingSpec( thickness=1, circle_radius=1 )
cap = cv2.VideoCapture( 0 )

with mp_face_mesh.FaceMesh( max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5 ) as face_mesh:
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
            captura_de_rostro = results.multi_face_landmarks[ 0 ]
            
            # Obtencion de las coordenadas de los puntos de interes
            coordenadas_punto_sup_ojo_derecho = captura_de_rostro.landmark[ FACEMESH_PUNTOS_OJO_DERECHO[ 0 ] ]
            coordenadas_punto_inf_ojo_derecho = captura_de_rostro.landmark[ FACEMESH_PUNTOS_OJO_DERECHO[ 1 ] ]
            coordenadas_punto_sup_ojo_izquierdo = captura_de_rostro.landmark[ FACEMESH_PUNTOS_OJO_IZQUIERDO[ 0 ] ]
            coordenadas_punto_inf_ojo_izquierdo = captura_de_rostro.landmark[ FACEMESH_PUNTOS_OJO_IZQUIERDO[ 1 ] ]

            # Calculo de la distancia entre los puntos de interes
            # distancia_ojo_derecho = coordenadas_punto_sup_ojo_derecho.y - coordenadas_punto_inf_ojo_derecho.y
            # distancia_ojo_izquierdo = coordenadas_punto_sup_ojo_izquierdo.y - coordenadas_punto_inf_ojo_izquierdo.y
            
            # Calculo de la distancia entre los puntos de interes usando la distancia euclidiana( Pitagoras )
            distancia_ojo_derecho = ( ( coordenadas_punto_sup_ojo_derecho.x - coordenadas_punto_inf_ojo_derecho.x ) ** 2 + ( coordenadas_punto_sup_ojo_derecho.y - coordenadas_punto_inf_ojo_derecho.y ) ** 2 ) ** 0.5
            distancia_ojo_izquierdo = ( ( coordenadas_punto_sup_ojo_izquierdo.x - coordenadas_punto_inf_ojo_izquierdo.x ) ** 2 + ( coordenadas_punto_sup_ojo_izquierdo.y - coordenadas_punto_inf_ojo_izquierdo.y ) ** 2 ) ** 0.5

            # Asignacion de las distancias calibradas
            distancia_calibrado_ojo_derecho = distancia_ojo_derecho
            distancia_calibrado_ojo_izquierdo = distancia_ojo_izquierdo

            # Grabar calibracion en archivo
            archivo.insertar_calibracion( distancia_calibrado_ojo_derecho, distancia_calibrado_ojo_izquierdo )
        else:
            print( "No se detecto rostro en la calibracion" )
            indicadores.no_se_detecto_rostro_en_calibrado()
                

    image.flags.writeable = True
    image = cv2.cvtColor( image, cv2.COLOR_RGB2BGR )
    if results.multi_face_landmarks:
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
