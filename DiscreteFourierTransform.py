import numpy as np
from matplotlib import pyplot as plt

SAMPLE_RATE = 44100  # Гц
DURATION = 5  # Секунды

def generate_sine_wave(freq, sample_rate, duration):
    x = np.linspace(0, duration, sample_rate*duration, endpoint=False)
    frequencies = x * freq
    # 2pi для преобразования в радианы
    y = np.sin((2 * np.pi) * frequencies)
    return x, y

# Генерируем волну с частотой 2 Гц, которая длится 5 секунд
# x, y = generate_sine_wave(2, SAMPLE_RATE, DURATION)
# plt.plot(x, y)
# plt.show()

'''
Микширование аудиосигналов состоит всего из двух этапов:

    cложение сигналов;
    нормализация результата.
'''

_, nice_tone = generate_sine_wave(400, SAMPLE_RATE, DURATION)
_, noise_tone = generate_sine_wave(4000, SAMPLE_RATE, DURATION)

noise_tone = noise_tone * 0.3
mixed_tone = nice_tone + noise_tone

'''
Символ подчеркивания (_) мы используем, чтобы отбросить значения x,
возвращаемые функцией generate_sine_wave() – нам не нужно складывать значения времени.

Следующий шаг – нормализация, масштабирование сигнала под целевой формат.
В нашем случае это 16-битное целое число в диапазоне от -32768 до 32767:
'''
normalized_tone = np.int16((mixed_tone / mixed_tone.max()) * 32767)

#plt.plot(normalized_tone[:1000])
#plt.show() # Видимая нами синусоидальная волна – это сгенерированный тон 400 Гц, искаженный тоном 4000 Гц.

from scipy.io.wavfile import write
#write("mysinewave.wav", SAMPLE_RATE, normalized_tone)


'''
Используем быстрое преобразование Фурье для удаления шума

Быстрое преобразование Фурье (FFT) – алгоритм, который позволяет вычислить частотный спектр сигнала:
'''

from scipy.fft import fft, fftfreq

# число точек в normalized_tone
N = SAMPLE_RATE * DURATION

# вычисление преобразования Фурье:
yf = fft(normalized_tone) #  вычисляет само преобразование
xf = fftfreq(N, 1/SAMPLE_RATE) # находит частоты в центре каждого «бина» на выходе fft()
# Под бином здесь понимается интервал значений, сгруппированных аналогично гистограмме.

# plt.plot(xf, np.abs(yf))
# plt.show() # Пики положительных частот находятся на позициях 400 и 4000 Гц.


"""
Примечание
Кстати, по графику можно заметить, что fft() возвращает в качестве максимальной частоты чуть
 более 20 тысяч герц, а именно: 22050 Гц. Это значение составляет ровно половину частоты 
 дискретизации и называется частотой Найквиста. Действительно, из фундаментальной теоремы
 обработки сигналов (теорема Котельникова), следует, что частота дискретизации должна как
 минимум вдвое превышать максимальную частоту сигнала.
""" 

# Обрабатываем сигнал еще быстрее с помощью rfft()

from scipy.fft import rfft, rfftfreq

# обратите внимание на r в начале имён функций
yf = rfft(normalized_tone)
xf = rfftfreq(N, 1/SAMPLE_RATE)

# plt.plot(xf, np.abs(yf))
# plt.show()


# Фильтрация сигнала
'''
Самая замечательная вещь в преобразовании Фурье заключается в том, что оно обратимо.
 Любой сигнал, измененный в частотной области, можно преобразовать обратно во временную
 область. Воспользуемся этим, чтобы отфильтровать высокочастотный шум.

Возвращаемые rfft() значения соответствуют мощности каждого частотного бина.
 Если мы установим мощность бина равной нулю, соответствующая частота перестанет
 присутствовать в результирующем сигнале во временной области:
'''
        
# Максимальная частота составляет половину частоты дискретизации
points_per_freq = len(xf) / (SAMPLE_RATE / 2)

# Наша целевая частота - 4000 Гц
target_idx = int(points_per_freq * 4000)

#Обнулим yf для индексов около целевой частоты:
        
yf[target_idx-2:target_idx+2] = 0

# plt.plot(xf, np.abs(yf))
# plt.show()

    

# Применение обратного преобразования Фурье

from scipy.fft import irfft

new_sig = irfft(yf)

# plt.plot(new_sig[:1000])
# plt.show()

norm_new_sig = np.int16(new_sig * (32767 / new_sig.max()))
write("clean.wav", SAMPLE_RATE, norm_new_sig)