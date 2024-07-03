import flet as ft
import requests as req

from pages import *
import components
import utility

def main(page: ft.Page):
    page.c = components
    page.u = utility
    page_index(page)

ft.app(main, port=80, view=None)