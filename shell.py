#######################################
# Date: 13.04.21                      #
# Auther: Idan Aviad                  #
# Summary: This file wait for input   #
#          and responde accordingly.  #
#######################################
import BBthon

while True:
  text = input('BBthon > ')
  result, error = BBthon.run('Not a file', text)

  if error: print(error)
  else: print(result)
