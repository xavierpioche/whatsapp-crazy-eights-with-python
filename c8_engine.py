#moteur
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import random
import cv2 as cv
import numpy as np
import subprocess
import time
import shutil
import os

localpath = 'E:\\apps\\'
pathtocards = 'E:\\apps\\boardgamePack_v2\\PNG\\Cards\\'
temporary = 'temporary.jpg'
telephonepath = 'Z:\DCIM\outbox\\'
localtemp = localpath + temporary
teleptemp = telephonepath + temporary
font = ImageFont.truetype('FreeMonoBold.ttf', 17)

#-----------------------------------------------------------------------

#players = {"xavier","chacha","olivia","laury"}
players = ["xavier","chacha","xavier","chacha"]

cards = [
    ['T','R','cardClubsK'],
    ['T','D','cardClubsQ'],
    ['T','V','cardClubsJ'],
    ['T','1','cardClubsA'],
    ['T','10','cardClubs10'],
    ['T','9','cardClubs9'],
    ['T','8','cardClubs8'],
    ['T','7','cardClubs7'],
    ['K','R','cardDiamondsK'],
    ['K','D','cardDiamondsQ'],
    ['K','V','cardDiamondsJ'],
    ['K','1','cardDiamondsA'],
    ['K','10','cardDiamonds10'],
    ['K','9','cardDiamonds9'],
    ['K','8','cardDiamonds8'],
    ['K','7','cardDiamonds7'],
    ['P','R','cardSpadesK'],
    ['P','D','cardSpadesQ'],
    ['P','V','cardSpadesJ'],
    ['P','1','cardSpadesA'],
    ['P','10','cardSpades10'],
    ['P','9','cardSpades9'],
    ['P','8','cardSpades8'],
    ['P','7','cardSpades7'],
    ['C','R','cardHeartsK'],
    ['C','D','cardHeartsQ'],
    ['C','V','cardHeartsJ'],
    ['C','1','cardHeartsA'],
    ['C','10','cardHearts10'],
    ['C','9','cardHearts9'],
    ['C','8','cardHearts8'],
    ['C','7','cardHearts7']
]

#print(cards)

indexesChar = [ 'A', 'Z', 'E', 'R', 'T', 'Y', 'U', 'O' ]
indexesNum = range(8)

indexCards = range(32)
new_IC = random.sample( indexCards, len(indexCards) )
new_PL = random.sample( players, len(players) )
#new_PL = players
print(new_IC)
print(new_PL)

game = [ [ new_PL[0], [ new_IC[0], new_IC[1], new_IC[2], new_IC[3], new_IC[4], new_IC[5], new_IC[6], new_IC[7] ] ],
    [ new_PL[1], [ new_IC[8], new_IC[9], new_IC[10], new_IC[11], new_IC[12], new_IC[13], new_IC[14], new_IC[15] ] ],
    [ new_PL[2], [ new_IC[16], new_IC[17], new_IC[18], new_IC[19], new_IC[20], new_IC[21], new_IC[22], new_IC[23] ] ],
    [ new_PL[3], [ new_IC[24], new_IC[25], new_IC[26], new_IC[27], new_IC[28], new_IC[29], new_IC[30], new_IC[31] ] ]
]

print(game)

sansfin=0
quiagagne = 0
aquiletour = 0
lastplayedcard = -1
lastplayedcardIMG = 'cardJoker'

card_length = 140 
card_height = 190
mode = 'RGB'
color = (255,255,255)

theboard = [ lastplayedcard ] # le tableau de ce qui a ete joue

while quiagagne == 0:
    # on genere la main du joueur
    j = 0
    k = 0
    who = game[aquiletour][0]
    print('c est au tour de ' + game[aquiletour][0] + ':')
    taille = len(game[aquiletour][1])
    if taille < 4: taille = 4 
    size = int(card_length * (( 1 + taille)/2))
    print('taille de l image :')
    print(size)
    blank_image = Image.new(mode, (size,2 * card_height + 40), color)
    draw = ImageDraw.Draw(blank_image)
    # on met la table
    table_large = len(theboard)
    table_tab = table_large
    print('taille de la table:' + str(table_large))
    if table_large > 4: table_large = 4 # on affiche que les 4 dernieres
    print('taille de la table suite:' + str(table_large))
    table_size = int(card_length * ((1 + table_large)/2))
    print('table size:' + str(table_size))
    table_milieu = int((size - table_size)/2)
    print('table_milieu:' + str(table_milieu))
    
    if table_tab < 4:
        they=0
    else:
        they = table_tab - table_large
    
    print('they=',str(they))
    thelastboard = theboard[they:]
    print('lastboard:')
    print(thelastboard)
    
    for u in thelastboard:
        if u == -1: 
            bcarte=lastplayedcardIMG
        else:
            bcarte=cards[u][2]
        im2 = Image.open(pathtocards + bcarte + '.png')
        blank_image.paste(im2, (table_milieu, 0))
        table_milieu = table_milieu + int(card_length/2)
    #
    print(game[aquiletour][1])
    memecoul=0 # pour savoir si le joueur peut jouer
    memefigu=0 # pour savoir si le joueur peut jouer
    for i in game[aquiletour][1]:
        # je construis la main
        print(cards[i])
        print('a rajouter ' + cards[i][2])
        if u == -1:
            memecoul=1
            memefigu=1
        else:
            if cards[i][0] == cards[u][0]: memecoul=1
            if cards[i][1] == cards[u][1]: memefigu=1    
        im2 = Image.open(pathtocards + cards[i][2] + '.png')
        blank_image.paste(im2, (j,card_height + 20))
        draw.text((j+20, card_height + 20 + card_height + 1), indexesChar[k], (0, 0, 0), font=font)
        j = j + int(card_length/2)
        k += 1
        print('j=',j)
    # la main est faite je l envoie
    #blank_image.show()
    blank_image.save(temporary)
    if os.path.exists(telephonepath + temporary): os.remove(telephonepath + temporary)
    shutil.copyfile('e:\\apps\\temporary.jpg', 'z:\\dcim\\outbox\\temporary.jpg')
    #blank_image.save(telephonepath + 'temp.jpg')
    # appel vers le programme find avec des parametres...
    # on verifie si le player n est pas boude, si oui on passe 2 en parametre 
    if (memecoul | memefigu): 
        thirdparam=0
    else: thirdparam=2
    
    print('thirdparam=' + str(thirdparam))
    #
    result = subprocess.run(['python','find.py',who,str(thirdparam)], capture_output=True)
    result = str(result.stdout)
    if len(result) == 8:
        reponse = result[2]
    else:
        reponse = -1
    print('>> la reponse est :')
    print(reponse)
    
    if reponse == -1 : 
        print('reponse: -1 // on passe son tour') 
        suite = 1
    else:
        # si -1, le jeu est casse on arrete tout
        
        #-----------------------------------------------------
        # on trouve l index de la lettre de reponse
        print('l index de la reponse est:')
        c_idx = indexesChar.index(reponse)
        print(c_idx)
        # on trouve l index de la carte dans main
        print('l index de la main est:')
        d_idx = game[aquiletour][1][c_idx]
        print(d_idx)
        #
        print('la carte est:')
        c_val = cards[d_idx]
        print(c_val)
        
        print('le board est:')
        print(theboard)
        
        suite = 0
        if lastplayedcard == -1:
            lastplayedcard = d_idx # attention on stock l index general de la carte 
            theboard.append(lastplayedcard)
            game[aquiletour][1].remove(lastplayedcard)
            print(game[aquiletour][1])
            suite = 1
        else:
            old_val = cards[lastplayedcard]
            print('old val=')
            print(old_val)
            if (c_val[0] == old_val[0]) or (c_val[1] == old_val[1]):
                suite = 1
                lastplayedcard = d_idx
                theboard.append(lastplayedcard)
                game[aquiletour][1].remove(lastplayedcard)
                print(game[aquiletour][1])
            else:
                suite = 0
            
        #
    if suite == 1:
        time.sleep(20) 
        aquiletour += 1
        if aquiletour > 3: aquiletour = 0
    sansfin += 1
    if sansfin > 50: quiagagne = 1

print(game)
#blank_image.show()
#blank_image.save('temp.jpg')

