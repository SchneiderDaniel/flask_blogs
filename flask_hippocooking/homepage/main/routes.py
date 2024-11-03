# from flask import render_template, request, redirect, url_for, send_from_directory, flash, Blueprint, current_app
from flask import Blueprint
from homepage.utils import get_current_time

main = Blueprint('main', __name__)


@main.route('/')
def index():
     return "Welcome to Hippocooking.com. This page is currently rebuild. Please visit us later this year. Current time of request: " + get_current_time()