# GraphVizualizer

# Как установить?
## 1) Установка pygame-ce
MacOS/Linux:
`pip3 install pygame-ce` 
Windows:
`pip install pygame-ce`

Теперь вы готовы запустить исходный файл main.py

## 2) Описание файла main.py
main.py - файл, содержащий главный код отвечающий за визуализацию.
Содержит 3 базовых класса:
1) **Node** - описывает вершину графа, ее цвет, имя, уникальный ID и позицию на экране (необходимо для сохранения графа в txt формат)
2) **Edge** - описывает ребро графа, хранит номер вершины откуда оно идет и куда
3) **Graph** - класс графа, содержит массив вершин и ребер, а так же сам граф, представленный в виде списка смежности

## 3) Использование 
Редактор позволяет редактировать граф при помощи клавиатуры и мыши.
Основные моменты:
- `Insert mode` - при нажатии клавиши i на клавиатуре включается так называемый insert mode (режим добавления вершин и ребер). Чтобы добавить вершину необходимо нажать в любом месте на экране правой кнопкой мыши, затем ввести имя новой вершины. Чтобы добавить ребро, достаточно протянуть его от одной вершины к другой, зажав при этом левую кнопку мыши
- `Normal mode` - при нажатии клавиши esc на клавиатуре включается "нормальный" режим. Тут вы можете двигать камеру, зажав колесико мыши(либо использовав клавиши WASD), выделять ноды левым кликом по ним(снять выделение - нажать esc), двигать ноды, зажав на них левую кнопку мыши.
- `Zoom` - вы можете приблизить или отдалить ваш граф, прокручивая колесико мыши
- `Save` - чтобы сохранить граф, нажмите cnrl + s, граф сохранится в папку, где лежит main.py в файл graph.txt
- `Algorithms.py` - файл, содержащий основные алгоритмы
##PS
файл graph.txt - файл содержащий граф Европы
файл MST2.txt - файл содержащий минимальное остовное дерево(чтобы его посмотреть в визуализаторе, можно изменить main.py для его открытия, либо просто переименовать его в graph.txt)
