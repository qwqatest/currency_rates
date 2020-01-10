
# Was taken here https://stackoverflow.com/questions/38282697/how-can-i-remove-0-of-float-numbers
def formatNumber(num):
  if num % 1 == 0:
    return int(num)
  else:
    return num