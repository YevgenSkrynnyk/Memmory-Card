#почни тут створювати додаток з розумними замітками
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QListWidgetItem, QLineEdit, QTextEdit, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QFormLayout, QInputDialog
import json

app = QApplication([])
notes_win = QWidget()
notes_win.setWindowTitle("Розумні замітки")
notes_win.resize(900,600)

#json
notes = {
    "Ласкаво просимо!" : {
        "текст": "kcz",
        "теги": ["привіт", "123456789"]
    }
}
with open("notes_data.json", "w") as file:
    json.dump(notes, file, sort_keys=True)


#Віджети
field_text = QTextEdit()#поле зліва

list_notes = QListWidget()
list_notes_label = QLabel("Список заміток")

list_tags = QListWidget()
list_tags_label = QLabel("Список тегів")

field_tag = QLineEdit()
field_tag.setPlaceholderText("Введіть тег...")

#кнопки для заміток
button_note_create = QPushButton("Створити замітку")
button_note_del = QPushButton("Видалити замітку")
button_note_save = QPushButton("Зберегти замітку")
#кнопки для тегів
button_tag_add = QPushButton("Додати тег")
button_tag_search = QPushButton("Шукати замітки по тегу")
button_tag_del = QPushButton("Відкріпити від замітки")

#Лайаути
layout_notes = QHBoxLayout()
col_1 = QVBoxLayout()
col_2 = QVBoxLayout()

col_1.addWidget(field_text)
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)

row_1 = QHBoxLayout()
row_2 = QHBoxLayout()
row_3 = QHBoxLayout()
row_4 = QHBoxLayout()
row_5 = QHBoxLayout()
row_6 = QHBoxLayout()

col_2.addLayout(row_1)
col_2.addLayout(row_2)



row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)

row_2.addWidget(button_note_save)

row_3.addWidget(field_tag)

col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)

row_5.addWidget(button_tag_add)
row_5.addWidget(button_tag_search)
row_6.addWidget(button_tag_del)

col_2.addLayout(row_1)
col_2.addLayout(row_2)
col_2.addLayout(row_3)
col_2.addLayout(row_4)
col_2.addLayout(row_5)
col_2.addLayout(row_6)

layout_notes.addLayout(col_1, stretch=2)
layout_notes.addLayout(col_2, stretch=1)
notes_win.setLayout(layout_notes)

def add_note():
    note_name, ok = QInputDialog.getText(notes_win, "Додати", "Назва замітки")
    if ok and note_name != "":
        notes[note_name] = {"текст": "", "теги": []}
        list_notes.addItem(note_name)
        list_tags.addItems(notes[note_name]["теги"])
        print(notes)

def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]["текст"] = field_text.toPlainText()
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys = True, ensure_ascii=False)
        print(notes)
    else:
        print("Замітка для збереження не вибрана!")

def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(notes)
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Замітка для збреження не вибрана!")

def show_note():
    key = list_notes.selectedItems()[0].text()
    field_text.setText(notes[key]["текст"])
    list_tags.clear()
    list_tags.addItems(notes[key]["теги"])

def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if not tag in notes[key]["теги"]:
            notes[key]["теги"].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Замітка не найдена")

def search_tag():
    print(button_tag_search.text())
    tag = field_tag.text()
    if button_tag_search.text() == "Шукати замітки по тегу" and tag:
        print(tag)
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]["теги"]:
                notes_filtered[note]=notes[note]
        button_tag_search.setText("Скинути пошук")
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
        print(button_tag_search.text())
    elif button_tag_search.text() == "Скинути пошук":
        field_tag.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
        button_tag_search.setText("Шукати замітки по тексту")
        print(button_tag_search.text())
    else:
        pass
def del_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]["теги"].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]["теги"])
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
    else:
        print("Замітка не вибрана")



button_note_create.clicked.connect(add_note)
button_note_save.clicked.connect(save_note)
button_note_del.clicked.connect(del_note)

button_tag_add.clicked.connect(add_tag)
button_tag_del.clicked.connect(del_tag)
button_tag_search.clicked.connect(search_tag)




with open("notes_data.json", "r") as file:
    notes = json.load(file)
list_notes.addItems(notes)
list_notes.itemClicked.connect(show_note)
notes_win.show()
app.exec_()