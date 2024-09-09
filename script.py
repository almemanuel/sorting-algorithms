import random
import datetime as dt
import pandas as pd
import time
import seaborn as sns
import matplotlib.pyplot as plt

def selection_sort(l):
    n = len(l)
    for j in range(n - 1):
        min_index = j
        for i in range(j, n):
            if l[i]['price'] < l[min_index]['price']:
                min_index = i
        if l[j]['price'] > l[min_index]['price']:
            l[j], l[min_index] = l[min_index], l[j]
            j += 1
    return l


def bubble_sort(l):
    n = len(l)
    for j in range(n-1):
        for i in range(n - 1):
            next_index = i + 1
            if l[i]['price'] > l[next_index]['price']:
                l[i], l[next_index] = l[next_index], l[i]
    return l


def insertion_sort(l):
    n = len(l)
    for i in range(1, n-1):
        key = l[i]
        j = i - 1
        while j >= 0 and l[j]['price'] > key['price']:
            l[j + 1] = l[j]
            j -= 1
        l[j + 1] = key
    return l


def merge_sort(l, start=0, end=None):
    if end is None:
        end = len(l)
    if(end - start > 1):
        half = (end + start)//2
        merge_sort(l, start, half)
        merge_sort(l, half, end)
        return merge(l, start, half, end)


def merge(l, start, half, end):
    left = l[start:half]
    right = l[half:end]
    top_left, top_right = 0, 0
    for k in range(start, end):
        if top_left >= len(left):
            l[k] = right[top_right]
            top_right = top_right + 1
        elif top_right >= len(right):
            l[k] = left[top_left]
            top_left = top_left + 1
        elif left[top_left]['price'] < right[top_right]['price']:
            l[k] = left[top_left]
            top_left = top_left + 1
        else:
            l[k] = right[top_right]
            top_right = top_right + 1
    return l


def generate_price():
    return random.uniform(0.01, 10000.0)


def generate_date():
    start = dt.date(dt.datetime.now().year, 1, 1)
    end = dt.date(dt.datetime.now().year, 12, 31)
    random_days = random.randint(0, (end - start).days)
    return start + dt.timedelta(days=random_days)


def generate_id():
    return random.randint(10000000, 99999999)


def generate_el():
    return {
        'price': generate_price(),
        'date': generate_date(),
        'id': generate_id()
    }


res = {'data': []}
times = []

for i in range(0, 100):
    size = random.randint(2, 10000)
    example = {
        'data': []
    }
    for j in range(0, size):
        example['data'].append(generate_el())
    start = time.time()
    res['data'] = selection_sort(example['data'])
    total = time.time() - start
    times.append(['selection', size, total])

    start = time.time()
    res['data'] = bubble_sort(example['data'])
    total = time.time() - start
    times.append(['bubble', size, total])

    start = time.time()
    res['data'] = insertion_sort(example['data'])
    total = time.time() - start
    times.append(['insertion', size, total])

    start = time.time()
    res['data'] = merge_sort(example['data'])
    total = time.time() - start
    times.append(['merge', size, total])

times = pd.DataFrame(times, columns=['alg', 'size', 'time'])
times['time_per_el'] = times['time'] / times['size']
times['time_per_el_normalized'] = (times['time_per_el'] - times['time_per_el'].min()) / (times['time_per_el'].max() - times['time_per_el'].min())
times['time_normalized'] = (times['time'] - times['time'].min()) / (times['time'].max() - times['time'].min())

plt.figure(figsize=(10, 6))
sns.boxplot(x='alg', y='time_normalized', data=times)
plt.title('Tempos de Execução por Algoritmo')
plt.xlabel('Algoritmo')
plt.ylabel('Tempo de Execução (s)')
plt.show()

plt.figure(figsize=(10, 6))
sns.barplot(x='alg', y='time_per_el_normalized', data=times, errorbar=None)
plt.title('Tempo Médio por Elemento')
plt.xlabel('Algoritmo')
plt.ylabel('Tempo Médio por Elemento (s)')
plt.show()

plt.figure(figsize=(10, 6))
sns.scatterplot(x='size', y='time_normalized', hue='alg', data=times, alpha=0.7)
plt.title('Tempo de Execução em Função do Tamanho da Entrada')
plt.xlabel('Tamanho da Entrada')
plt.ylabel('Tempo de Execução (s)')
plt.show()

example = pd.DataFrame(example['data'])
example.sort_values('price', ascending=False, inplace=True)