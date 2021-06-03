#######################################
# Date: 13.04.21                      #
# Author: Idan Aviad                  #
# Summary: This file wait for input   #
#          and responde accordingly.  #
#######################################
import BBthon

while True:
  text = input('BBthon> ')
  if text.strip() == "": continue
  result, error = BBthon.run('.ץבוק אל הז הא', text)

  if error: print(error)
  elif result: 
    if len(result.elements) == 1:
      print(repr(result.elements[0]))
    else:
      print(repr(result))