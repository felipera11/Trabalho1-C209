import PySimpleGUI as sg
import os.path
from paste import convert

sg.theme("DarkBlue14")

personDIR = str('')
backgroundDIR = str('')

#cria a coluna de importar o arquivo
file_list_column = [
    #importação do arquivo de fundo
    [
        sg.Text("BG Folder"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER1-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 10), key="-FILE LIST1-"
        )
    ],
    #importação do arquivo de pessoa
    [
        sg.Text("Person Folder"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER2-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 10), key="-FILE LIST2-"
        )
    ],
    #botão de converter
    [
        sg.Button("Converter", key="-GRABCUT-")
    ]
]

#cria a coluna de visualização da imagem
image_viewer_column = [
    [sg.Text("Choose an image from list on left:")],
    [sg.Image(key="-IMAGE-")]

]

#criando o layout
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeparator(),
        sg.Column(image_viewer_column),
    ]
]

#abre a janela
window = sg.Window("Image Viewer", layout)

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    #quando seleciona a pasta, mostra uma lista de arquivos
    if event == "-FOLDER1-":
        folder = values["-FOLDER1-"]
        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".png", ".gif", ".jpg", "jpeg"))
        ]
        
        window["-FILE LIST1-"].update(fnames)
    #quando seleciona o arquivo
    elif event == "-FILE LIST1-": 
        try:
            filename = values["-FILE LIST1-"][0]
            backgroundDIR = filename

        except:
            pass

    #quando seleciona a pasta, faz uma lista de arquivos
    elif event == "-FOLDER2-":
        folder = values["-FOLDER2-"]
        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".png", ".gif", ".jpg", ".jpeg"))
        ]
        window["-FILE LIST2-"].update(fnames)
    #quando seleciona o arquivo
    elif event == "-FILE LIST2-": 
        try:
            filename = values["-FILE LIST2-"][0]
            personDIR = filename
            
        except:
            pass

    #quando o botao de converter é pressionado, chama a função de converter e atualiza a imagem da direita
    elif event == "-GRABCUT-":
       
        convert(backgroundDIR,personDIR)
        window["-IMAGE-"].update('result.png')


window.close()