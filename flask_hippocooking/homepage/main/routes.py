# from flask import render_template, request, redirect, url_for, send_from_directory, flash, Blueprint, current_app
from flask import render_template
from . import main

@main.route('/')
def index():
     return render_template('index.html')