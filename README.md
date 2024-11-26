# Cats

Приложение для визуализации перемещения котов и их состояний в зависимости от расстояния относительно друг друга.

Коты могут находиться в одном из следующих состояний:
> - WALK (гуляет, базовое состояние)
> - HISS (шипит)
> - FIGHT (дерется)
> - EAT (ест)
> - HIT (ударился)
> - SLEEP (спит)

![Cats (Ubuntu) 2024-11-22 16-30-20 (2)](https://github.com/user-attachments/assets/d5ea91f9-3200-4f97-bf48-954bcc5b5caa)

## Запуск приложения
Необходимо установить Anaconda.

Далее в директории проекта:
```
conda env create -f environment.yml
conda activate catsenv
python ui/ui.py
```

## Системные требования
Поддержка CUDA 12.6.
