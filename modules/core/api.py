import time
import sys
import os
import django
from django.http import Http404
from django.shortcuts import render
from libs.default.core import BaseController
from libs.default import GamesRetro
from GamesRetro import settings
from django.core.management import call_command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GameRetro.settings")


class ConfigurationsController(BaseController):

    def load_games(self, request):
        print('SOU REQUEST',request)
        form = request.method
        print(form)
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
                response = GamesRetro.list_roms(emulator,emulador)
            elif action == '2':
                self.response = GamesRetro.page_rom(emulator,emulador,game)
                return self.response
            elif action == 'sair' or action == 'Sair' or action == 'SAIR':
                print('\nSaindo...')
                time.sleep(2)
                sys.exit(0)
        else:
            print('Comando inválido,tente novamente!!!')

    def open_games(self, request):
        print('SOU REQUEST',request)
        form = request.method
        print(form)
        url = request.GET.get('url')
        console = request.GET.get('change_console')
        print('SOU GET',url,console)
        GamesRetro.load_start(console, url)
        return render(request,"games/Nesbox.html")

    def open_nesbox1(self, request):
        return render(request,"games/nesbox/embed.html")

    def open_nesbox(self, request):
        #from libs.JoyMapper import joy
        #django.setup()
        #call_command('joy')
        return render(request,"games/Nesbox.html")


class AbstractAPI:

    def filter_request(request, formulary=None):
        if request.is_ajax() or settings.DEBUG:
            if formulary is not None:
                form = formulary(request.POST)
                if form.is_valid():
                    return True, form
                else:
                    return False, form
            else:
                return True,True
        else:
            raise Http404