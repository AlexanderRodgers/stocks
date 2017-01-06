import csv
import urllib.request

with open('apple2016.csv') as csvfile:
    file = csv.reader(csvfile, delimiter=',')
    
    date = []
    change = []

    first_line = True
    for row in file:
        if first_line:
            first_line = False
            continue
        
        s_date = row[0]
        open = float(row[1])
        close = float(row[4])
        daily_change = open - close
        
        date.append(s_date)
        change.append(daily_change)


max_val = change[0]

for index, val in enumerate(change):
    print(index)
    if val > max_val:
        max_val = val
        max_ind = index
    
print('apple highest:', max_val)
print('date of highest:', date[max_ind])

best_performance = date[max_ind]

end,middle,start = best_performance.split('-')

print('formatted date', start, middle, end)

custom_url = ("https://www.google.com/search?q=" + "apple" + "stock&source=lnt&tbs=cdr%3A1%2Ccd_min%3A" + start
            + "%2F" + middle +  "%2F" + end + "%2Ccd_max%3A" + 
            start + "%2F" + middle +  "%2F" + end + "&tbm=")