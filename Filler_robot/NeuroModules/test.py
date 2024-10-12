import cv2
import numpy as np

# Функция для обновления изображений и ключевых точек
def compare_images_feature_matching(nfeatures, contrastThreshold, edgeThreshold):
    # Получение изображения из камеры
    # image_1 = self.camera.image_copy
    # image_2 = self.camera.read_cam()

    image_1 = cv2.imread('cropped_image.png')
    image_2 = cv2.imread('cropped_image_2.png')

    # Преобразование изображений в оттенки серого
    image_1_gray = cv2.cvtColor(image_1, cv2.COLOR_BGR2GRAY)
    image_2_gray = cv2.cvtColor(image_2, cv2.COLOR_BGR2GRAY)

    # Обрезка изображений
    cropped_image_1 = image_1_gray
    cropped_image_2 = image_2_gray 

    # Инициализация SIFT детектора
    print(edgeThreshold)
    sift = cv2.SIFT_create(nfeatures = nfeatures, contrastThreshold = contrastThreshold, edgeThreshold = edgeThreshold)

    # Нахождение ключевых точек и дескрипторов
    kp1, des1 = sift.detectAndCompute(cropped_image_1, None)
    kp2, des2 = sift.detectAndCompute(cropped_image_2, None)

    

    # Проверка, что дескрипторы не пустые
    if des1 is None or des2 is None:
        print("Дескрипторы пустые. Проверьте изображения и параметры детектора.")
        return False
    
    print('len(kp1)', len(kp1), len(kp2))

    if len(kp2) >= len(kp1) * 0.33:
        print('Стакан есть')
    else:
        print('Стакан нету')


    # Рисование ключевых точек на обрезанных изображениях
    cropped_image_1_with_keypoints = cv2.drawKeypoints(cropped_image_1, kp1, None, flags=cv2.DrawMatchesFlags_DRAW_RICH_KEYPOINTS)
    cropped_image_2_with_keypoints = cv2.drawKeypoints(cropped_image_2, kp2, None, flags=cv2.DrawMatchesFlags_DRAW_RICH_KEYPOINTS)

    # Сохранение изображений с нарисованными ключевыми точками
    cv2.imwrite('cropped_image_1_with_keypoints.png', cropped_image_1_with_keypoints)
    cv2.imwrite('cropped_image_2_with_keypoints.png', cropped_image_2_with_keypoints)
    cv2.imshow('Controls', cropped_image_1_with_keypoints)
    cv2.imshow('Controls2', cropped_image_2_with_keypoints)
    # # Инициализация BFMatcher
    # bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)

    # # Сопоставление дескрипторов
    # matches = bf.match(des1, des2)

    # # Сортировка совпадений по расстоянию
    # matches = sorted(matches, key=lambda x: x.distance)
    # num_matches = len(matches)

    # # Максимально возможное количество совпадений
    # max_matches = min(len(kp1), len(kp2))

    # # Процент совпадений
    # if max_matches != 0:
    #     match_percentage = (num_matches / max_matches) * 100
    # else:
    #     match_percentage = 0  # или любое другое значение, которое имеет смысл в вашем контексте

    # # Результат сравнения
    # result = match_percentage >= 80

    # print(f'Сходство: {result}, {match_percentage}')

    # return result


# Создание окна для ползунков
cv2.namedWindow('Controls')
cv2.namedWindow('Controls2')

# Создание ползунков для настройки параметров
cv2.createTrackbar('nfeatures', 'Controls', 1337, 10000, lambda x: None)
cv2.createTrackbar('contrastThreshold', 'Controls', 13, 100, lambda x: None)
cv2.createTrackbar('edgeThreshold', 'Controls', 33, 100, lambda x: None)

# Основной цикл для обновления изображений и ключевых точек
while True:
    # Получение текущих значений ползунков
    nfeatures = cv2.getTrackbarPos('nfeatures', 'Controls')
    contrastThreshold = cv2.getTrackbarPos('contrastThreshold', 'Controls') / 1000.0
    edgeThreshold = cv2.getTrackbarPos('edgeThreshold', 'Controls') 

    # Обновление изображений и ключевых точек
    compare_images_feature_matching(nfeatures, contrastThreshold, edgeThreshold)

    # Ожидание нажатия клавиши для выхода
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Закрытие всех окон
cv2.destroyAllWindows()