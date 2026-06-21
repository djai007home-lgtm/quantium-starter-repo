import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# This automatically downloads the correct chromedriver matching your local Google Chrome version
# and places it exactly where Dash/Selenium can find it.
os.environ["PATH"] += os.pathsep + os.path.dirname(ChromeDriverManager().install())

from dash.testing.composite import DashComposite
from app import app  # Imports your layout and callback from app.py


# 1. Test that the main header exists and has the correct text
def test_header_present(dash_duo: DashComposite):
    dash_duo.start_server(app)
    header = dash_duo.wait_for_element("h1")
    assert header.text == "Pink Morsel Sales Visualiser"


# 2. Test that the line chart visualization is loaded
def test_visualization_present(dash_duo: DashComposite):
    dash_duo.start_server(app)
    visualization = dash_duo.wait_for_element("#sales-line-chart")
    assert visualization is not None


# 3. Test that our region filter buttons are present
def test_region_picker_present(dash_duo: DashComposite):
    dash_duo.start_server(app)

    btn_north = dash_duo.wait_for_element("#btn-north")
    btn_east = dash_duo.wait_for_element("#btn-east")
    btn_south = dash_duo.wait_for_element("#btn-south")
    btn_west = dash_duo.wait_for_element("#btn-west")
    btn_all = dash_duo.wait_for_element("#btn-all")

    assert btn_north is not None
    assert btn_east is not None
    assert btn_south is not None
    assert btn_west is not None
    assert btn_all is not None