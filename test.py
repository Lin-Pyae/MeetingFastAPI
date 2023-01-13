from datetime import datetime

current = datetime.now()
test = datetime(2023,1,13,14,41,44)
final = current-test
print("current : ",current)
print("test : ", test)
print(final.total_seconds())