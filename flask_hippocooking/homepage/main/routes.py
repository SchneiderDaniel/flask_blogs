# from flask import render_template, request, redirect, url_for, send_from_directory, flash, Blueprint, current_app
from flask import Blueprint

main = Blueprint('main', __name__)


@main.route('/')
def index():
     return "Hello, World Hippocooking!"