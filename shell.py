#######################################
# Date: 13.04.21                      #
# Author: Idan Aviad                  #
# Summary: This file wait for input   #
#          and responde accordingly.  #
#######################################
import BBthon

while True:
  text = input('BBthon> ')
  result, error = BBthon.run('.ץבוק אל הז הא', text)

  if error: print(error)
  elif result: print(repr(result))
