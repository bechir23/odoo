import os

def install():
    print("Installing Internship Management Module...")
    os.system('odoo-bin -u internship_management')
    print("Installation complete.")