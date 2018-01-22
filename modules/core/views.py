import sys
import time
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from libs.default import GamesRetro

# Create your views here.


def index(request):
    return render(request,"games/GamesRetro.html")

def view_roms(request):
    print('SOU REQUEST',request)
    form = request.method
    print(form)
    print(request.POST)
    change_console = request.POST.get('change-console')
    rom_name = request.POST.get('q')
    print('SOU GET',change_console,rom_name)
    emulador = GamesRetro.console(change_console)
    print(emulador)
    emulator = GamesRetro.set_emulador(emulador)
    print(emulator)
    game = GamesRetro.game_rom(rom_name)
    print(game)
    if game is not None:
        action = '2'
    if action == '1':
        GamesRetro.list_roms(emulator,emulador)
    elif action == '2':
        response = GamesRetro.page_rom(emulator,emulador,game)
        #print('SOU RESPONSE:',response)
        #print('SOU RESPONSE:',response['name_rom'],response['url_rom'])
        #response = response['name_rom']
    elif action == 'sair' or action == 'Sair' or action == 'SAIR':
        print('\nSaindo...')
        time.sleep(2)
        sys.exit(0)
    else:
        print('Comando inválido,tente novamente!!!')
    return render(request,"games/search_roms.html",{'response': response})
