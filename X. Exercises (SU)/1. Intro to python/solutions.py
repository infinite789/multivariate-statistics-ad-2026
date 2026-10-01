import random
import numpy as np
import matplotlib.pyplot as plt


def christmas_tree(n):
    if not 2 <= n <= 100:
        return
    star_row = n * ' ' + '✶' + n * ' '
    print(star_row)
    for branches in range(1, n + 1):
        # този цикъл се върти за всеки ред в дръвчето
        # branches е колко клончета има от едната страна, минава от 0 до n
        spaces = n - branches # колко спейса има преди и след клончетата
        left_side = ' ' * spaces + '/' * branches # страната на дървото преди стеблото |
        right_side = '\\' * branches + ' ' * spaces # страната на дървото преди стеблото |. Трябва да използваме \\, понеже само \ е специален символ, с който се означават специалните символи (например \n е нов ред). 
        print(left_side + '|' + right_side)
    trunk_row = n * ' ' + '|' + n * ' '
    print(trunk_row)
        
        
def monte_carlo_ln(n):
    # генерираме n на брой независими точки в квадрата 1 <= x <= 2, 0 <= y <= 1. 
    # (тук се иска y и x да са само некорелирани. Генерирането на произволни числа е доста бавно. Как можем да направим тази функция по-бърза?)
    x = [1 + random.random() for _ in range(n)]
    y = [random.random() for _ in range(n)]
    hits = 0
    for i in range(n):
        if y[i] < 1 / x[i]:
            hits += 1
    return hits / n


def np_carlo_ln(n):
    x = 1 + np.random.random(n)
    y = np.random.random(n)
    return (x * y < 1).sum() / n

def generate_np_carlo_samples(n, k):
    return np.array([np_carlo_ln(n) for _ in range(k)])

def sample_statistics(samples):
    print(f"Min = {samples.min()}")
    print(f"Max = {samples.max()}")
    print(f"Mean = {samples.mean():.4f}")
    print(f"Median = {np.median(samples)}") # samples.median() няма
    print(f"Std = {samples.std():.4e}") # scientific notation
    quantiles = np.quantile(samples, [i/4 for i in range(1, 4)])
    print(f"First quantile = {quantiles[0]}")
    print(f"Third quantile = {quantiles[2]}")


def blackjack_score():
    scores = [i for i in range(2, 10)] + [10] * 4 + [11] # масив с 13 елемента, даващ точките на всички карти от 2 до А
    cards = np.repeat(scores, 4) # numpy масив с всички елементи на scores повторени по 4 пъти (52 елемента, т.е. всички карти в тестето
    cards_repeated = np.vstack([cards for _ in range(cards.shape[0])]) # матрица 52х52 от горния вектор повторен 52 пъти
    two_card_combos = np.vstack([[cards_repeated], [cards_repeated.T]]).T # тензор 52х52х2 от горната матрица и транспонираната горна матрица. Двумерните вектори са всички комбинации от две карти
    two_card_scores = two_card_combos.sum(axis=2) # матрица 52х52 от точките на всички комбинации от две карти
    two_card_scores = np.tril(two_card_scores, k=1).flatten() # зануляваме елементите над диагонала и взимаме всички стойности като едномерен масив. По диагонала са комбинации от една и съща карта (невъзможно), а над диагонала са същите комбинации като отдолу.
    two_card_scores = two_card_scores[two_card_scores != 0] # махаме всички нули
    two_card_scores[two_card_scores == 22] = 12 # заместваме точките на две аса с 12 (асото може да е 11 или 1, искаме да сме под 21 точки)
    return two_card_scores.mean(), two_card_scores.std() # можем да върнем две стойности едновременно. Ще върне tuple
    
 
# Горната функция приема, че всички комбинации от карти са равновероятни. 
# Оправдан ли е този избор? Ако не, как може да променим функцията, за да поддържа различна вероятност за кобинациите от карти?


np_carlo_color_pallete = np.array(['b', 'r'])
def pretty_np_carlo_ln(n):
    x = 1 + np.random.random(n)
    y = np.random.random(n)
    is_under_plot = x * y < 1
    color = np_carlo_color_pallete[is_under_plot.astype(int)] 
    # above line will take np_carlo_color_pallete[0] if point is not under the plot 
    # and np_carlo_color_pallete[1] if it is under the plot
    plt.scatter(x, y, c=color, s=1)
    plot_x = np.linspace(1, 2, 1000) # 1000 equally spaced points from 1 to 2
    plt.plot(plot_x, 1 / plot_x, c='g', linewidth=3)
    return (is_under_plot).sum() / n
