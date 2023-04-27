import cv2 
import mediapipe

#Desenhando os pontos via mediapipe
drawing_hands = mediapipe.solutions.drawing_utils
#Definindo o estilo dos pontos via mediapipe
drawing_styles_hands = mediapipe.solutions.drawing_styles
#Detecta as mãos da imagem
detect_hands = mediapipe.solutions.hands

#Função para pegar o movimento das mãos e identificar qual a jogada da mão direita
def identify_movement_hand_right(identify_hands):
    #Identificando pontos de referencia das mãos
    landmarks = identify_hands.landmark
    #Identificando pelos pontos de refencia se é Tesoura
    if (landmarks[5].x > landmarks[8].x) and (landmarks[9].x > landmarks[12].x) and (landmarks[13].x > landmarks[16].x) and (landmarks[17].x > landmarks[20].x): return "Rock"
    #Identificando pelos pontos de refencia se é Pedra
    if (landmarks[5].x < landmarks[8].x) and (landmarks[9].x < landmarks[12].x) and (landmarks[13].x < landmarks[16].x) and (landmarks[17].x < landmarks[20].x): return "Paper"
    #Identificando pelos pontos de refencia se é Papel
    else: return "Scissors"
#Função para pegar o movimento das mãos e identificar qual a jogada da mão esquerda
def identify_movement_hand_left(identify_hands):
    #Identificando pontos de referencia das mãos
    landmarks = identify_hands.landmark
    #Identificando pelos pontos de refencia se é Tesoura
    if (landmarks[5].x < landmarks[8].x) and (landmarks[9].x < landmarks[12].x) and (landmarks[13].x < landmarks[16].x) and (landmarks[17].x < landmarks[20].x): return "Rock"
    #Identificando pelos pontos de refencia se é Pedra
    if (landmarks[5].x > landmarks[8].x) and (landmarks[9].x > landmarks[12].x) and (landmarks[13].x > landmarks[16].x) and (landmarks[17].x > landmarks[20].x): return "Paper"
    #Identificando pelos pontos de refencia se é Papel
    else: return "Scissors"

#Abrindo o vídeo na tela
vid = cv2.VideoCapture("pedra-papel-tesoura.mp4")
#Textos do vídeo
text=""
#Placar do jogador da direita
scoreboard_right = 0
#Placar do jogador da direita
scoreboard_left = 0
#Tempo de jogo
clock = 0

#Achando as mãos no video pedra-papel-tesoura.mp4
with detect_hands.Hands(model_complexity=0, min_detection_confidence=0.5,min_tracking_confidence=0.5) as detecting_hands:
    while True:
        #Lendo o vídeo
        ret, frame = vid.read()
        #Caso o vídeo não abra irá quebrar
        if not ret or frame is None: break
        #Transformando o vídeo em RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #Detecta as mãos na imagem
        detecting = detecting_hands.process(frame)
        #Transformando a imagem em BGR
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        #Realizando um if para detectar as duas mãos
        if detecting.multi_hand_landmarks:
            #Iremos fazer um for para que ele identifique cada ponto dentro das mãos
            for hand_landmarks in detecting.multi_hand_landmarks:
                #Desenhando os macros na mão
                drawing_hands.draw_landmarks(frame, hand_landmarks, detect_hands.HAND_CONNECTIONS, drawing_styles_hands.get_default_hand_landmarks_style(), drawing_styles_hands.get_default_hand_connections_style())
        
        #Guardando os macros de referencia
        hands_detected = detecting.multi_hand_landmarks
        #Verificando se a quantidade de mãos está correta no vídeo
        if hands_detected and len(hands_detected) == 2:
            #Irá pegar o movimento do jogador um da mão da direita
            player1_identify = identify_movement_hand_right(hands_detected[0])
            #Irá pegar o movimento do jogador dois da mão da esquerda
            player2_identify = identify_movement_hand_left(hands_detected[1])
            #Verifica o ganhador da partida
            if ret:
                if player1_identify == player2_identify:
                    text = "Draw"
                elif player1_identify == "Paper" and player2_identify == "Rock":
                    text = "Player 1 Winner"
                elif player1_identify == "Paper" and player2_identify == "Scissors":
                    text = "Player 2 Winner"
                elif player1_identify == "Rock" and player2_identify == "Scissors":
                    text = "Player 1 Winner"
                elif player1_identify == "Rock" and player2_identify == "Paper":
                    text = "Player 2 Winner"
                elif player1_identify == "Scissors" and player2_identify == "Paper":
                    text = "Player 1 Winner"
                elif player1_identify == "RoScissorsck" and player2_identify == "Rock":
                    text = "Player 2 Winner"
                else:
                    print("Nobody Wins")
            else:
                ret = False
            #Adicionando o placar no game
            clock = (clock + 1) % 180
            #Fazendo a logica para que o placar funcione
            clock += 1
            #Fazendo a condição para adicionar no placar do game
            if clock >= 120 and clock <= 120.5:
                #Condição para o Player 2 ganhador
                if text == "Player 1 Winner":
                    scoreboard_left += 1
                #Condição para o Player 1 ganhador
                elif text == "Player 2 Winner":
                    scoreboard_right += 1
                #Placar empatado
                else:
                    scoreboard_left == scoreboard_right
                    scoreboard_right == scoreboard_left

        #Adicionando os texts no jogo
        cv2.putText(frame, text, (600, 950), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 2)
        #Adicionando o texto do player 1
        cv2.putText(frame, str("Player 1"), (150, 150), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 4)
        #Adicionando os texto do player 2
        cv2.putText(frame, str("Player 2"), (1000, 150), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 4)
        #Adicionando movimento player 1
        cv2.putText(frame, player1_identify, (150, 300), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 4)
        #Adicionando movimento player 2
        cv2.putText(frame, player2_identify, (1000, 300), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 4)
        #Adicionando o placar player 1
        cv2.putText(frame, str(scoreboard_left), (150, 400), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 4)
        #Adicionando o placar player 2
        cv2.putText(frame, str(scoreboard_right), (1000, 400), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 4)

        cv2.imshow('Game', frame)
        #Pausando o vídeo
        if cv2.waitKey(1) & 0xFF == ord('q'): break


vid.release()
cv2.destroyAllWindows()