
import cv2
import os
import pytesseract
from PIL import Image
import sys
import numpy as np
import argparse


pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'

# The list of allergens in 4 languages: English, French, Russian, and Spanish
IallergicEng=['Gluten','milk','peanuts','Soy','tuna','Eggs','Fish','nuts','tonsils']
IallergicFra=['Gluten', 'lait', 'cacahuètes', 'soja', 'thon', 'œufs', 'poisson', 'noix', 'amygdales']
IallergicRus=['Глютен', 'молоко', 'арахис', 'соя', 'тунец', 'яйца', 'рыба', 'орехи', 'миндалины']
IallergicSpa=['Gluten', 'leche', 'maní', 'soja', 'atún', 'huevos', 'pescado', 'nueces', 'amígdalas']



'''
Image processing function:
Gets 3 parameters: the list of index of allergens for testing,
 the path of the image to be tested,
and the processing language
 
 Return Bool if an allergen is found, and return a list of found allergens.
'''
def Answer_processing(arrAllerg, path, lang):

  if path=="galleryToCameraPage.png":
      return "Product image not captured, please return to previous step"

  # Arranging the path
  path = path.replace('\\\\', "/")
  path = path.replace("[\'", "")
  path = path.replace("\']", "")
  image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)#Black and white
  cv2.imwrite('thresh.png', image)

  img = Image.open('thresh.png')

  #Optimal resolution for the process according to tests we did
  width, heightS = img.size
  new_size = width*3, heightS*3
  img = img.resize(new_size, Image.LANCZOS)
  img = img.point(lambda x:0 if x < 128 else 200, '1')

  # Use OCR to read the text from the image  according to the language selected

  if lang=="English":
    dataA = pytesseract.image_to_string(img, lang='eng')
    arrAllergLang=IallergicEng
  if lang == "Spanish":
      dataA = pytesseract.image_to_string(img, lang='spa')
      arrAllergLang = IallergicSpa
  if lang == "Russian":
      dataA = pytesseract.image_to_string(img, lang='rus')
      arrAllergLang = IallergicRus
  if lang == "French":
      dataA = pytesseract.image_to_string(img, lang='fra')
      arrAllergLang = IallergicFra


#Download markings that will interfere with the identification of the text
#according to tests we have done
  punctuations = '''!()[]{};:'"\,<>./?@#$%^&*_~'''
  data = ""
  for char in dataA:
      if char not in punctuations:
          data+= char
  print(data)  # for us
  # Unity in uppercase and lowercase letters
  dataLower = data.lower()

  dataArry= dataLower.split()#Division into an array
  whyNot=""
  caneat=True


  #We will go through the list of allergens from the user and look in the text layout
  for i in arrAllerg:#The user's list
      word=arrAllergLang[int(i)]#find the allerg according the language selected
      wlower = word.lower()
      for j in dataArry:
          jlower = j.lower()

          if wlower==jlower :#the allerg found in data
              whyNot+=word+', '
              caneat = False
              break;
              #Allergens with 2 writing forms
          if wlower=='soy' and jlower=='soya':
              whyNot += word + ', '
              caneat = False
              break;
          if wlower == 'eggs' and jlower == 'egg':
                  whyNot += word + ', '
                  caneat = False
                  break;
          if wlower=='gluten' and jlower=='wheat':
              whyNot += word + ', '
              caneat = False
              break;

  whyNot=whyNot[:-2]


  return whyNot,caneat

