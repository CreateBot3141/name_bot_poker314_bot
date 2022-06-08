
def send_message (user_id,namebot,hand2,message_id):
    import iz_telegram
    import time
    if 1==1:
        markup = ''

        message_out,menu = iz_telegram.get_message (user_id,'Сообщение 1 Ваши карты',namebot)
        message_out = message_out.replace('%%Ваши карты%%',str(hand2))  
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,message_id)


        time.sleep (2)

        answer = iz_telegram.bot_send (user_id,namebot,str(hand2.game_cards),markup,0)
        time.sleep (2)
        answer = iz_telegram.bot_send (user_id,namebot,str(hand2.game_name),markup,0)
        message_out,menu,answer  = iz_telegram.send_message (user_id,namebot,'Ваша ставка','S',0) 

def save_game (summ):
    from hand import hand
    from player import player
    from deck import deck
    from utils import compare_games
    from card import card   
    import iz_func 
    db,cursor = iz_func.connect ()
    if 1==1:
        my_deck = deck()
        my_deck.shuffle()
        card1 = my_deck.draw(5) 
        card2 = my_deck.draw(5)
        markup = ''
        #card3 = my_deck.draw(2)
        hand1 = hand(card1)
        hand2 = hand(card2)
        me1 = player(hand1)
        me2 = player(hand2)
        table = [me1,me2]
        table = compare_games(table)
        winner = table[0]
        result = 'нет данных' 
        if winner.hand.cards == hand1.cards:
            result = 'Проиграли'
        if winner.hand.cards == hand2.cards:    
            result = 'Победа'            
        hand_save_1 = '' 
        for line in hand1.cards:
            hand_save_1 = hand_save_1 + str(line.label)+';'+str(line.suit)+';'+str(line.value)+':'
        hand_save_2 = '' 
        for line in hand2.cards:
            hand_save_2 = hand_save_2 + str(line.label)+';'+str(line.suit)+';'+str(line.value)+':'
        sql = "INSERT INTO game_poker (`hand1`,`hand2`,`winner`,summ) VALUES ('{}','{}','{}',{})".format (iz_func.change(str(hand_save_1)),iz_func.change(str(hand_save_2)),result,summ)
        cursor.execute(sql)
        db.commit()
    return hand1,hand2

def start_prog (user_id,namebot,message_in,status,message_id,name_file_picture,telefon_nome):
    import time
    import iz_func
    import iz_game
    import iz_telegram

    from hand import hand
    from player import player
    from deck import deck
    from utils import compare_games
    from card import card       
    db,cursor = iz_func.connect ()
   
    if message_in == 'Кошелёк':
        #message_out,menu,answer  = iz_telegram.send_message (user_id,namebot,'Ваш баланс','S',0)
        message_out,menu = iz_telegram.get_message (user_id,'Ваш баланс',namebot)
        balans = iz_telegram.get_balans (user_id,namebot,'RUB')
        message_out      = message_out.replace('%%Баланс%%',str(balans))
        markup = ''
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0)

    if message_in.find ('/start') != -1:    	
        iz_func.save_variable (user_id,"status","",namebot)
        iz_telegram.language (namebot,user_id)
        status = ''

    if message_in.find ('Отмена') != -1:
        iz_func.save_variable (user_id,"status","",namebot)
        status = ''
        message_out,menu,answer  = iz_telegram.send_message (user_id,namebot,'ОтменаЗапуск','S',0)
        label = 'no send'

    if message_in =='Начать партию':
        message_out,menu,answer  = iz_telegram.send_message (user_id,namebot,'Раздача карт','S',0)

    if message_in =='50 рублей':
        summ     = -50
        comment  = 'Ставка за игру'
        currency = 'RUB'
        iz_telegram.add_money (namebot,user_id,summ,comment,currency)
        hand1,hand2 = save_game (summ)
        message_out,menu,answer  = iz_telegram.send_message (user_id,namebot,'Начальная ставка','S',message_id)
        send_message (user_id,namebot,hand2,message_id) 

    if message_in =='100 рублей':
        summ     = -100
        comment  = 'Ставка за игру'
        currency = 'RUB'
        iz_telegram.add_money (namebot,user_id,summ,comment,currency)
        hand1,hand2 = save_game (summ)
        message_out,menu,answer  = iz_telegram.send_message (user_id,namebot,'Начальная ставка','S',message_id)
        send_message (user_id,namebot,hand2,message_id) 

    if message_in =='300 рублей':
        summ     = -300
        comment  = 'Ставка за игру'
        currency = 'RUB'
        iz_telegram.add_money (namebot,user_id,summ,comment,currency)
        hand1,hand2 = save_game (summ)
        message_out,menu,answer  = iz_telegram.send_message (user_id,namebot,'Начальная ставка','S',message_id)
        send_message (user_id,namebot,hand2,message_id) 



    if message_in =='Пасс':
        message_out,menu,answer  = iz_telegram.send_message (user_id,namebot,'Ждем Вас в новой игре','S',message_id) 

    if message_in =='Играю':
        message_out,menu,answer  = iz_telegram.send_message (user_id,namebot,'Ставка сделана','S',message_id) 
        summ     = -100
        comment  = 'Ставка за полную игру'
        currency = 'RUB'
        iz_telegram.add_money (namebot,user_id,summ,comment,currency)        
        sql = "select id,hand1,hand2,winner from game_poker where 1=1;".format()
        cursor.execute(sql)
        data = cursor.fetchall()
        for rec in data: 
            id,hand1,hand2,winner = rec.values() 
        card_x  = hand1.split(':')
        card_x1 = card_x[0].split(';')
        card_x2 = card_x[1].split(';')
        card_x3 = card_x[2].split(';')
        card_x4 = card_x[3].split(';')
        card_x5 = card_x[4].split(';')
        card1   = card (card_x1[0],card_x1[1],card_x1[2])
        card2   = card (card_x2[0],card_x2[1],card_x2[2])
        card3   = card (card_x3[0],card_x3[1],card_x3[2])
        card4   = card (card_x4[0],card_x4[1],card_x4[2])
        card5   = card (card_x5[0],card_x5[1],card_x5[2])
        hand1  =  hand([card1,card2,card3,card4,card5])
        markup = ''
        answer = iz_telegram.bot_send (user_id,namebot,str(hand1),markup,0)
        time.sleep (2)
        answer = iz_telegram.bot_send (user_id,namebot,str(hand1.game_cards),markup,0)
        time.sleep (2)
        answer = iz_telegram.bot_send (user_id,namebot,str(hand1.game_name),markup,0)
        answer = iz_telegram.bot_send (user_id,namebot,str(winner),markup,0)

        if winner == 'Победа':  
            summ     = 400
            comment  = 'Победа'
            currency = 'RUB'
            iz_telegram.add_money (namebot,user_id,summ,comment,currency)        




