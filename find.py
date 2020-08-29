from __future__ import print_function
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController
from PIL import ImageGrab, Image 
from imagesearch import *

import pytesseract
import filecmp
import sys
import cv2 as cv
import autopy
import time
import numpy as np


use_mask = False
img = None
templ = None
mask = None
image_window = "Source Image"
result_window = "Result window"
match_method = cv.TM_SQDIFF_NORMED
max_Trackbar = 5

keyboard = KeyboardController()
mouse = MouseController()


def main(argv):
    
    global img
    global templ
    
    if (len(sys.argv) < 2):
        print('Not enough parameters')
        print('Usage:\nfind.py <user> ')
        return -1
    
    debug = 0
    passesontour = 0
    if (len(sys.argv) == 2):
        if sys.argv[2] == 1: 
            debug=1
            passesontour=0
        elif sys.argv[2] == 2: 
            debug=0 
            passesontour=1
    
    #img = cv.imread(sys.argv[1], cv.IMREAD_COLOR)
    ##############################################################
    # est ce qu on est sur la page principale
    if (debug): print('> Est-ce qu on est sur le menu principal ?')
    laloop = 1
    num = 0
    while laloop == 1:
        printscreen_pil =  ImageGrab.grab()
        printscreen_numpy =   np.array(printscreen_pil.getdata(),dtype='uint8')\
            .reshape((printscreen_pil.size[1],printscreen_pil.size[0],3)) 
        RGB_img = cv.cvtColor(printscreen_numpy, cv.COLOR_BGR2RGB)
    ##cv.imshow('window',RGB_img)
    #cv.imwrite('screengrab.bmp',RGB_img)
    #//
    #img = cv.imread('screengrab.bmp', cv.IMREAD_COLOR)
        sub_img = RGB_img[630:690,370:427].copy() # pour whatsapp
    ##cv.imshow('cropped', sub_img)
    # on cree ici l icone de reference à chercher apres
    #cv.imwrite('wicon.bmp', sub_img)
    
        templ = cv.imread('wicon.bmp', cv.IMREAD_COLOR)
    
        result = mse(sub_img, templ)
        if (debug): print(result)
    
        if result > 1: # on n est pas sur la page principale
            if (debug): print('> non, alors on appuie sur le bouton home')
            mouse.position = (30,30)
            mouse.press(Button.middle)
            mouse.release(Button.middle)
            time.sleep(5)
            if num == 10: break
        else:
            if (debug): print('> ca y est on peut appuyer sur whatsapp')
            mouse.position = (0,0)
            time.sleep(2)
            mouse.position = (387,650)
            time.sleep(2)
            #mouse.position = (100,100)=80,80
            mouse.press(Button.left)
            mouse.release(Button.left)
            laloop = 0
        num += 1

    ##############################################################
    # on est maintenant sur whatsapp 
    # hauteur des cellule 148 (112) -> 233 (180) = 85 (68)
    time.sleep(2)
    laloop = 1
    num = 0
    # est-ce qu'on est sur la page principale de whatsapp
    while laloop == 1 : 
        pos = imagesearch('whatsapp.bmp')
        if pos[0] != -1:
            mouse.position = (10,100) #on y est, on ne fait rien
            laloop = 0
        else:
            mouse.position = (13, 56) #11,45
            mouse.press(Button.left)
            mouse.release(Button.left)
            if num == 10: break 
            num += 1
        
    ##-- a qui le tour ?    
    #print(">> ba ki moun ou vlé palé ?")
    #who = input()
    # 
    who = sys.argv[1]
    time.sleep(2)
    ##--- /// Nouvelle Sequence
    time.sleep(2)
    pyautogui.moveTo(357,65) # position de l icone search
    mouse.press(Button.left)
    mouse.release(Button.left)
    time.sleep(2)
    keyboard.type(who)
    time.sleep(2)
    pyautogui.moveTo(119,155) # position de l icone du user 
    mouse.press(Button.left)
    mouse.release(Button.left)
    time.sleep(2)
    pyautogui.moveTo(345,885) # position de l icone hide keyboard
    mouse.press(Button.left)
    mouse.release(Button.left)
    time.sleep(2)
    #// il faut verifier que c est la bonne personne ?
    
    ##--- ///Ancienne sequence
    #pos = imagesearch(who + ".bmp")
    #pos = imagesearch("xavier.bmp")
    #if pos[0] != -1:
    #    print("position : ", pos[0], pos[1])
    #    pyautogui.moveTo(pos[0]+50, pos[1]+20)
    #    mouse.press(Button.left)
    #    mouse.release(Button.left)
    #else:
    #    print("user not found")
    
    ###### debug_start on revient sur whatsapp
    #pyautogui.moveTo(170,500)
    #mouse.press(Button.left)
    #mouse.release(Button.left)
    ##### debug_end a cause des input, apres plus besoin en full automatique
    
    #-----------------
    # il faut recuperer l image a envoyer à l utilisateur recherche
    # ??? how ?
    
    
    #///> DEBUT DE LA SEQUENCE D ENVOI <///
    # on fait la sequence d envoi de l image de outbox
    # Ce PC\Galaxy J4+\Phone\DCIM\outbox
    time.sleep(2)
    pyautogui.moveTo(318,851) # position de l icone attach
    mouse.press(Button.left)
    mouse.release(Button.left)
    time.sleep(2)
    pyautogui.moveTo(322,605) # position de l icone galerie
    mouse.press(Button.left)
    mouse.release(Button.left)
    time.sleep(2)
    pyautogui.moveTo(312,505) # position de l icone outbox
    mouse.press(Button.left)
    mouse.release(Button.left)
    time.sleep(2)
    pyautogui.moveTo(51,179) # position de l icone du board
    mouse.press(Button.left)
    mouse.release(Button.left)
    time.sleep(2)
    pyautogui.moveTo(388,768) # position de l icone envoyer
    mouse.press(Button.left)
    mouse.release(Button.left)
    time.sleep(2)
    pyautogui.moveTo(24, 63) #11,45  # retour au menu whatsapp
    #<mouse.press(Button.left)
    #<mouse.release(Button.left)
    time.sleep(2)
    #///> FIN DE LA SEQUENCE D ENVOI <///
    
    
    # ------------------------------------------
    # j ecris un message
    #print(">> ka ou bizwin di'y?")
    #what = input()
    ###### debug_start on revient sur whatsapp
    #pyautogui.moveTo(170,500)
    #mouse.press(Button.left)
    #mouse.release(Button.left)
    ##### debug_end a cause des input, apres plus besoin en full automatique
    #time.sleep(1)
    #keyboard.type(what)
    #mouse.position = (426,853)
    #mouse.press(Button.left)
    #mouse.release(Button.left)
    # ------------------------------------------
    
    
    # On verifie si on a une réponse
    if passesontour:
        reponse=-2
        time.sleep(2)
        keyboard.type('desole tu es boude, on passe ton tour')
        time.sleep(1)
        pyautogui.moveTo(411,825) # position de l icone envoyer
        mouse.press(Button.left)
        mouse.release(Button.left)
    else:
        for r in range(3):
            time.sleep(30) 
            printscreen_pil =  ImageGrab.grab()
            printscreen_numpy =   np.array(printscreen_pil.getdata(),dtype='uint8')\
                .reshape((printscreen_pil.size[1],printscreen_pil.size[0],3)) 
            RGB_img = cv.cvtColor(printscreen_numpy, cv.COLOR_BGR2RGB)
            #
            #imd1 = Image.fromarray(RGB_img)
            #imd1.save('rgbimg.jpg')
            sub_img = RGB_img[772:800,24:44].copy()
            #imd2 = Image.fromarray(sub_img)
            #imd2.save('subimg.jpg')
            #
            #custom_config = r'-c tessedit_char_whitelist=azertyuiAZERTYUI --psm 6'
            custom_config = r'-c tessedit_char_whitelist=AZERTYUO --psm 6'
            reponse = pytesseract.image_to_string(sub_img, config=custom_config) 
            #print(reponse)
            if len(reponse) > 1: reponse = reponse[0]
            #print(reponse)
            valid_chars = {"A","Z","E","R","T","Y","U","O"} 
            if reponse in valid_chars:
                if (debug): print('on va jouer la carte de l index ' + reponse)
                break 
            #return reponse 
            else:
                if (debug): print('la lettre n est pas valide')
                keyboard.type('la reponse n est pas valide')
                time.sleep(1)
                pyautogui.moveTo(411,825) # position de l icone envoyer
                mouse.press(Button.left)
                mouse.release(Button.left)
                reponse = -1       
    print(reponse)
    return 0 
 
 
def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err
    
if __name__ == "__main__":
    main(sys.argv[1:])