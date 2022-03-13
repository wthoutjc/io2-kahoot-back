class Puntaje():
    def __init__(self, time_test):
        self.id = None
        self.answers = None
        self.puntaje = 0

        self.time_test = time_test

    def set_id(self, id):
        self.id = id

    def set_answers(self, answers):
        self.answers = answers

    def descompose(self, str):
        result = ''
        for a in str:
            if a == ":":
                pass
            else:
                result += a
        return int(result)

    def calificar(self):
        '''
        Califica el examén y añade un puntaje competitivo
        en base al tiempo de respuesta
        '''
        # Iterar keys
        print('CALIFICAR')
        if self.answers == None:
            return self.puntaje
        self.puntaje = 0
        for keys in self.answers.items():
            print(keys)
            #Question 1 - ANSWER C
            if keys[0] == 'question1':
                # Respuesta correcta
                if keys[1][0] == 3:
                    self.puntaje += self.descompose(keys[1][1])
            #Question 2 - ANSWER A
            if keys[0] == 'question2':
                # Respuesta correcta
                if keys[1][0] == 1:
                    self.puntaje += self.descompose(keys[1][1])
            #Question 3 - ANSWER C
            if keys[0] == 'question3':
                # Respuesta correcta
                if keys[1][0] == 3:
                    self.puntaje += self.descompose(keys[1][1])
            #Question 4 - ANSWER D
            if keys[0] == 'question4':
                # Respuesta correcta
                if keys[1][0] == 4:
                    self.puntaje += self.descompose(keys[1][1])
            #Question 5 - ANSWER B
            if keys[0] == 'question5':
                # Respuesta correcta
                if keys[1][0] == 2:
                    self.puntaje += self.descompose(keys[1][1])
        return self.puntaje
